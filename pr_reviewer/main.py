import subprocess
import tempfile
from pathlib import Path
from contextlib import contextmanager

from .utils import Settings

import typer

CODE_EXTENSIONS = {".py", ".yaml", ".yml", ".toml", ".json"}

OTHER_FILES = {"README.md", "Dockerfile", "Makefile"}

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

        if file.suffix in CODE_EXTENSIONS or file.name in OTHER_FILES:
            try:
                content = file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                sections.append("_Binary or non-UTF8 file contents omitted_\n")
                continue

            parsed = parse_code(content)
            sections.append(parsed)

        else:
            sections.append("_Non-code file contents omitted_\n")

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


def _git_diff(repo_path: Path, target: str) -> str:
    return subprocess.check_output(
        ["git", "diff", f"origin/{target}", "HEAD", "--minimal"],
        cwd=repo_path,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def get_diff_by_file(repo_path: Path) -> list[str]:
    try:
        diff = _git_diff(repo_path, "main")
    except subprocess.CalledProcessError as main_exception:
        print(f"get_diff_by_file.subprocess.CalledProcessError.{main_exception = }")
        try:
            diff = _git_diff(repo_path, "master")
        except subprocess.CalledProcessError as master_exception:
            print(
                f"get_diff_by_file.subprocess.CalledProcessError.{master_exception = }"
            )
            raise RuntimeError(
                "Failed to get git diff against 'main' or 'master'"
            ) from master_exception

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
    user_context: str,
    coding_rules: str,
    flattened_codebase: str,
    diffs: list[str],
) -> str:
    diffs_block = "\n\n".join(f"```{diff}\n```" for diff in diffs)

    return """
You are a Pull Request Reviewer AI agent.
You will be given:

- User Context (optional) to understand specific criteria for this review
- A number of coding rules to check against the code changes
- A snapshot of the repository regarding all relevant files
- Code changes to review

Your output must be a JSON object with the following structure:

```json
{{
    "approved": boolean,
    "change_requests": [
        {{
            "file": "path/to/file.ext",
            "line": 123,
            "comment": "Description of the issue and suggested improvement"
        }}
    ],
    "summary": "A brief summary of what the PR changes seem to be trying to achieve, and any concerns or positive feedback you have about the implementation",
}}
```

================================================================================

# User context

{user_context}

================================================================================

# Coding Rules

{coding_rules}

================================================================================

# Repository Snapshot

{flattened_codebase}

================================================================================

# Code Changes

{diffs_block}
""".strip().format(
        user_context=user_context,
        coding_rules=coding_rules,
        flattened_codebase=flattened_codebase,
        diffs_block=diffs_block,
    )


def _fetch_branch(repo_path: Path, branch: str) -> bool:
    try:
        subprocess.check_call(
            ["git", "fetch", "origin", branch],
            cwd=repo_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


@contextmanager
def clone_branch(repo_url: str, branch: str):
    with tempfile.TemporaryDirectory(prefix="pr-reviewer-") as tmp_dir:
        repo_path = Path(tmp_dir)

        try:
            # Clone ONLY the PR branch
            subprocess.check_call(
                [
                    "git",
                    "clone",
                    "--branch",
                    branch,
                    repo_url,
                    str(repo_path),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )

            fetched = _fetch_branch(repo_path, "main") or _fetch_branch(
                repo_path, "master"
            )

            if not fetched:
                raise RuntimeError("Could not fetch base branch 'main' or 'master'")

        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Failed to prepare repository '{repo_url}@{branch}'"
            ) from exc

        yield repo_path


def get_rules() -> str:
    rules_dir = Settings.CODING_RULES_PATH
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


def get_partitioned_calls(system_prompt: str, diffs: list[str]) -> list[str]:
    if (len(system_prompt) / 4) < Settings.MAX_TOKENS_CONTEXT_WINDOW:
        return [system_prompt]

    print(f"Prompt exceeds context window, diffs are size: {len(diffs) / 4:,} tokens")

    return [system_prompt]  # TO DO: placeholder until actual implementation
