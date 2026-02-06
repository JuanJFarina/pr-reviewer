import subprocess
import tempfile
from pathlib import Path
from contextlib import contextmanager

import typer

CODE_EXTENSIONS = {".py", ".yaml", ".yml", ".toml", ".json", ".md"}

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
}


def retrieve_flattened_codebase(path: Path) -> str:
    sections: list[str] = []

    for file in sorted(path.rglob("*")):
        if any(part in EXCLUDED_DIRS for part in file.parts):
            continue

        if not file.is_file():
            continue

        relative_path = file.relative_to(path).as_posix()
        sections.append(f"## {relative_path}")

        if file.suffix in CODE_EXTENSIONS:
            try:
                content = file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                sections.append("_Binary or non-UTF8 file omitted_\n")
                continue

            parsed = parse_code(content)
            sections.append(parsed)

        sections.append("")  # spacing

    return "\n".join(sections)


def parse_code(file_content: str) -> str:
    lines = file_content.rstrip().splitlines()

    numbered_lines = [f"{i + 1:4d} | {line}" for i, line in enumerate(lines)]

    return "\n".join(
        [
            "```",
            *numbered_lines,
            "```",
        ]
    )


def _git_diff(target: str) -> str:
    return subprocess.check_output(
        ["git", "diff", f"{target}...HEAD"],
        text=True,
    )


def get_diff_by_file() -> list[str]:
    try:
        diff = _git_diff("main")
    except subprocess.CalledProcessError as main_exception:
        print(f"get_diff_by_file.subprocess.CalledProcessError.{main_exception = }")
        try:
            diff = _git_diff("master")
        except subprocess.CalledProcessError as master_exception:
            print(
                f"get_diff_by_file.subprocess.CalledProcessError.{master_exception = }"
            )
            raise RuntimeError(
                "Failed to get git diff against 'main' or 'master'"
            ) from master_exception

    print(f"get_diff_by_file.{diff = }")

    files: list[str] = []
    current: list[str] = []

    for line in diff.splitlines():
        if line.startswith("diff --git"):
            if current:
                files.append("\n".join(current))
                current = []
        current.append(line)

    if current:
        files.append("\n".join(current))

    return files


def get_system_prompt(
    user_instructions: str,
    flattened_codebase: str,
    diffs: list[str],
) -> str:
    diffs_block = "\n\n".join(
        f"### Diff {i + 1}\n```diff\n{diff}\n```" for i, diff in enumerate(diffs)
    )

    return f"""
You are a senior software engineer performing a strict pull request review.

## User Instructions
{user_instructions}

## Repository Snapshot
{flattened_codebase}

## Code Changes
{diffs_block}

## Task
- Identify bugs, risks, and design issues
- Suggest improvements
- Reference exact file paths and line numbers
- Be concise, precise, and actionable
""".strip()


@contextmanager
def clone_branch(repo_url: str, branch: str):
    with tempfile.TemporaryDirectory(prefix="pr-reviewer-") as tmp_dir:
        repo_path = Path(tmp_dir)

        try:
            subprocess.check_call(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "--branch",
                    branch,
                    "--single-branch",
                    repo_url,
                    str(repo_path),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Failed to clone branch '{branch}' from '{repo_url}'"
            ) from exc

        yield repo_path


def get_rules() -> str:
    rules_dir = Path("coding_rules")
    sections: list[str] = []

    if not rules_dir.exists():
        return ""

    for md in sorted(rules_dir.glob("*.md")):
        content = md.read_text(encoding="utf-8")
        sections.append(f"## {md.name}\n{content.strip()}")

    return "\n\n".join(sections)


def parse_repo_ref(repo_ref: str) -> tuple[str, str]:
    if "@" not in repo_ref:
        raise typer.BadParameter(
            "Repository reference must be in the form 'repo-url@branch'"
        )

    repo_url, branch = repo_ref.rsplit("@", 1)

    if not repo_url or not branch:
        raise typer.BadParameter(
            "Invalid repository reference. Expected 'repo-url@branch'"
        )

    return repo_url, branch
