from typing import Annotated

import typer

from polar_cli import __version__
from polar_cli.config import Environment, OutputFormat
from polar_cli.context import CliContext

app = typer.Typer(
    name="polar",
    help="Polar CLI — manage products, customers, and webhooks from the terminal.",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"polar {__version__}")
        raise typer.Exit()


@app.callback()
def main_callback(
    ctx: typer.Context,
    base_url: Annotated[
        str | None,
        typer.Option("--base-url", envvar="POLAR_BASE_URL", help="Custom API base URL (for self-hosted)."),
    ] = None,
    sandbox: Annotated[
        bool,
        typer.Option("--sandbox", help="Use the sandbox environment."),
    ] = False,
    output: Annotated[
        OutputFormat,
        typer.Option("--output", "-o", help="Output format: table, json, yaml."),
    ] = OutputFormat.TABLE,
    no_color: Annotated[
        bool,
        typer.Option("--no-color", help="Disable colored output."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose output."),
    ] = False,
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True, help="Show version and exit."),
    ] = None,
) -> None:
    ctx.obj = CliContext(
        environment=Environment.from_sandbox_flag(sandbox),
        output_format=output,
        base_url=base_url,
        verbose=verbose,
        no_color=no_color,
    )


# Import and register sub-commands
from polar_cli.commands.auth import app as auth_app  # noqa: E402
from polar_cli.commands.benefit_grants import app as benefit_grants_app  # noqa: E402
from polar_cli.commands.benefits import app as benefits_app  # noqa: E402
from polar_cli.commands.checkout_links import app as checkout_links_app  # noqa: E402
from polar_cli.commands.checkouts import app as checkouts_app  # noqa: E402
from polar_cli.commands.custom_fields import app as custom_fields_app  # noqa: E402
from polar_cli.commands.customers import app as customers_app  # noqa: E402
from polar_cli.commands.discounts import app as discounts_app  # noqa: E402
from polar_cli.commands.disputes import app as disputes_app  # noqa: E402
from polar_cli.commands.event_types import app as event_types_app  # noqa: E402
from polar_cli.commands.events import app as events_app  # noqa: E402
from polar_cli.commands.files import app as files_app  # noqa: E402
from polar_cli.commands.license_keys import app as license_keys_app  # noqa: E402
from polar_cli.commands.members import app as members_app  # noqa: E402
from polar_cli.commands.meters import app as meters_app  # noqa: E402
from polar_cli.commands.metrics import app as metrics_app  # noqa: E402
from polar_cli.commands.orders import app as orders_app  # noqa: E402
from polar_cli.commands.org import app as org_app  # noqa: E402
from polar_cli.commands.payments import app as payments_app  # noqa: E402
from polar_cli.commands.products import app as products_app  # noqa: E402
from polar_cli.commands.refunds import app as refunds_app  # noqa: E402
from polar_cli.commands.subscriptions import app as subscriptions_app  # noqa: E402
from polar_cli.commands.webhooks import app as webhooks_app  # noqa: E402

app.add_typer(auth_app)
app.add_typer(org_app)
app.add_typer(products_app)
app.add_typer(customers_app)
app.add_typer(orders_app)
app.add_typer(subscriptions_app)
app.add_typer(webhooks_app)
app.add_typer(checkout_links_app)
app.add_typer(checkouts_app)
app.add_typer(discounts_app)
app.add_typer(benefits_app)
app.add_typer(license_keys_app)
app.add_typer(meters_app)
app.add_typer(metrics_app)
app.add_typer(events_app)
app.add_typer(refunds_app)
app.add_typer(custom_fields_app)
app.add_typer(payments_app)
app.add_typer(disputes_app)
app.add_typer(benefit_grants_app)
app.add_typer(event_types_app)
app.add_typer(files_app)
app.add_typer(members_app)


def main() -> None:
    app()
