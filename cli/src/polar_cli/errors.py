"""Error handler decorator — catches SDK exceptions and renders clean messages."""

from __future__ import annotations

import functools
import json
from typing import Any, Callable

import httpx
import typer
from polar_sdk.models import PolarError, SDKError
from pydantic import ValidationError
from rich.console import Console

console = Console(stderr=True)


def _format_validation_errors(exc: ValidationError) -> str:
    """Format Pydantic validation errors into readable messages."""
    messages = []
    for error in exc.errors():
        loc = ".".join(str(x) for x in error["loc"])
        msg = error["msg"]
        messages.append(f"  {loc}: {msg}")
    return "\n".join(messages)


def _format_api_error(body: str | dict[str, Any] | None) -> str:
    """Format API error response into readable message."""
    if body is None:
        return "Unknown error"

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return body

    if isinstance(body, dict):
        # Handle Polar validation errors
        if "detail" in body and isinstance(body["detail"], list):
            messages = []
            for detail in body["detail"]:
                if isinstance(detail, dict):
                    loc = ".".join(str(x) for x in detail.get("loc", []))
                    msg = detail.get("msg", "")
                    if loc and msg:
                        messages.append(f"  {loc}: {msg}")
                    elif msg:
                        messages.append(f"  {msg}")
            if messages:
                return "\n".join(messages)

        # Handle simple error message
        if "error" in body:
            error_type = body.get("error", "")
            if "detail" in body and isinstance(body["detail"], str):
                return f"{error_type}: {body['detail']}"
            return error_type

        return json.dumps(body, indent=2)

    return str(body)


def handle_errors(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that catches common exceptions and prints user-friendly messages."""

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)
        except (typer.Exit, typer.Abort):
            raise
        except ValidationError as exc:
            console.print("[bold red]Validation error:[/bold red]")
            console.print(_format_validation_errors(exc))
            raise typer.Exit(1) from None
        except SDKError as exc:
            console.print(f"[bold red]API error ({exc.status_code}):[/bold red]")
            console.print(_format_api_error(exc.body))
            raise typer.Exit(1) from None
        except PolarError as exc:
            # PolarError subclasses may have a body attribute with JSON error
            if hasattr(exc, "body") and exc.body:
                console.print("[bold red]API error:[/bold red]")
                console.print(_format_api_error(exc.body))
            else:
                console.print(f"[bold red]Error:[/bold red] {exc}")
            raise typer.Exit(1) from None
        except httpx.ConnectError as exc:
            console.print("[bold red]Connection failed:[/bold red]")
            console.print(f"  Could not connect to API server")
            raise typer.Exit(1) from None
        except httpx.TimeoutException:
            console.print("[bold red]Request timed out:[/bold red]")
            console.print(f"  The server took too long to respond")
            raise typer.Exit(1) from None
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
            raise typer.Exit(1) from None

    return wrapper
