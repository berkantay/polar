"""Tests for the root app — global flags, version, help."""

from __future__ import annotations

from typer.testing import CliRunner

from polar_cli import __version__
from polar_cli.app import app

runner = CliRunner()


class TestVersion:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert f"polar {__version__}" in result.output


class TestHelp:
    def test_no_args_shows_usage(self):
        result = runner.invoke(app, [])
        # no_args_is_help=True returns exit code 2 (usage error)
        assert result.exit_code == 2
        assert "Usage:" in result.output

    def test_help_flag(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "--sandbox" in result.output
        assert "--output" in result.output
        assert "--base-url" in result.output


class TestOutputValidation:
    def test_invalid_output_format_rejected(self):
        result = runner.invoke(app, ["--output", "xml", "org", "list"])
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    def test_valid_output_formats_accepted(self):
        # These will fail with auth errors, but the important thing is
        # they don't fail with "Invalid value" for --output
        for fmt in ("table", "json", "yaml"):
            result = runner.invoke(app, ["--output", fmt, "org", "list"])
            assert "Invalid value" not in result.output


class TestSandboxFlag:
    def test_sandbox_flag_accepted(self):
        result = runner.invoke(app, ["--sandbox", "auth", "status"])
        # Will fail with "Not authenticated" but sandbox flag itself is fine
        assert "Invalid" not in result.output


class TestSubcommandHelp:
    def test_all_commands_have_help(self):
        commands = [
            "auth", "org", "products", "customers", "orders",
            "subscriptions", "webhooks", "checkout-links", "checkouts",
            "discounts", "benefits", "license-keys", "meters",
            "metrics", "events", "refunds", "custom-fields",
            "payments", "disputes", "benefit-grants", "event-types",
            "files", "members",
        ]
        for cmd in commands:
            result = runner.invoke(app, [cmd, "--help"])
            assert result.exit_code == 0, f"{cmd} --help failed: {result.output}"
