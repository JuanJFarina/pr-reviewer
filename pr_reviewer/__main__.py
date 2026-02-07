import typer

from .main import (
    retrieve_flattened_codebase,
    get_diff_by_file,
    get_system_prompt,
    get_rules,
    clone_branch,
    parse_repo_ref,
)

app = typer.Typer(
    add_completion=False,
    help="LLM-friendly Pull Request reviewer",
)


@app.command()
def main(
    repo: str = typer.Argument(
        ...,
        help="Repository reference in the form 'repo-url@branch'",
    ),
    context: str | None = typer.Option(
        None,
        "--context",
        help="Optional user instructions to guide the PR review",
    ),
):
    repo_url, branch = parse_repo_ref(repo)

    typer.echo(f"Reviewing PR from branch '{branch}'")
    typer.echo(f"Repository: {repo_url}")

    with clone_branch(repo_url, branch) as repo_path:
        typer.echo("Flattening codebase...")
        flattened_codebase = retrieve_flattened_codebase(repo_path)

        typer.echo("Collecting diffs...")
        diffs = get_diff_by_file()

    typer.echo("Loading coding rules...")
    rules = get_rules()

    typer.echo("Building system prompt...")
    system_prompt = get_system_prompt(
        user_instructions=context or "",
        flattened_codebase=f"{rules}\n\n{flattened_codebase}",
        diffs=diffs,
    )

    typer.echo("\n" + "=" * 80 + "\n")
    typer.echo(system_prompt)
    typer.echo("\n" + "=" * 80 + "\n")
    typer.echo(f"Token Count: {len(system_prompt) // 4:,}")
    typer.echo("\n" + "=" * 80)


if __name__ == "__main__":
    app()
