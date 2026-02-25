"""Error handler decorator — catches SDK exceptions and renders clean messages."""

from __future__ import annotations

import functools
from typing import Any, Callable

import httpx
import typer
from polar_sdk.models import PolarError, SDKError
from rich.console import Console

console = Console(stderr=True)


def handle_errors(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that catches common exceptions and prints user-friendly messages."""

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)
        except (typer.Exit, typer.Abort):
            raise
        except SDKError as exc:
            console.print(
                f"[bold red]API Error ({exc.status_code}):[/bold red] {exc.body or exc.message}"
            )
            raise typer.Exit(1) from None
        except PolarError as exc:
            console.print(f"[bold red]SDK Error:[/bold red] {exc}")
            raise typer.Exit(1) from None
        except httpx.ConnectError as exc:
            console.print(f"[bold red]Connection failed:[/bold red] {exc}")
            raise typer.Exit(1) from None
        except httpx.TimeoutException as exc:
            console.print(f"[bold red]Request timed out:[/bold red] {exc}")
            raise typer.Exit(1) from None
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
            raise typer.Exit(1) from None

    return wrapper
