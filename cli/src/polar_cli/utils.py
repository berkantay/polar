"""Shared helpers — org resolution, spinners."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

import typer
from rich.console import Console
from rich.status import Status

from polar_cli.config import OutputFormat, get_default_org_id
from polar_cli.context import get_cli_context

console = Console(stderr=True)


def resolve_org_id(ctx: typer.Context, org_flag: str | None) -> str:
    """Resolve the organization ID from the --org flag or default config.

    Returns the org ID string. Exits with error if neither is available.
    """
    if org_flag:
        return org_flag

    cli_ctx = get_cli_context(ctx)
    default = get_default_org_id(cli_ctx.environment)
    if default:
        return default

    console.print(
        "[bold red]No organization specified.[/bold red] "
        "Pass [bold]--org <id>[/bold] or set a default with [bold]polar org set-default <id>[/bold]."
    )
    raise typer.Exit(1)


@contextmanager
def spinner(message: str) -> Generator[Status, None, None]:
    """Show a spinner while a long operation runs."""
    with console.status(message, spinner="dots") as status:
        yield status


def get_output_format(ctx: typer.Context) -> OutputFormat:
    return get_cli_context(ctx).output_format
