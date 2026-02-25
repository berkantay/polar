"""Tests for org commands."""

from __future__ import annotations

from unittest.mock import MagicMock

from tests.conftest import make_list_result


class TestOrgList:
    def test_list(self, runner, cli_app, mock_polar):
        org = MagicMock()
        org.id = "org-1"
        org.slug = "my-org"
        org.name = "My Org"
        org.created_at = "2024-01-01"

        mock_polar.organizations.list.return_value = make_list_result([org])

        result = runner.invoke(cli_app, ["org", "list"])
        assert result.exit_code == 0
        assert "My Org" in result.output


class TestOrgGet:
    def test_get(self, runner, cli_app, mock_polar):
        org = MagicMock()
        org.id = "org-1"
        org.slug = "my-org"
        org.name = "My Org"
        org.avatar_url = None
        org.created_at = "2024-01-01"

        mock_polar.organizations.get.return_value = org

        result = runner.invoke(cli_app, ["org", "get", "org-1"])
        assert result.exit_code == 0
        assert "My Org" in result.output


class TestOrgSetDefault:
    def test_set_default(self, runner, cli_app, mock_polar, mocker):
        org = MagicMock()
        org.id = "org-1"
        org.slug = "my-org"
        org.name = "My Org"

        mock_polar.organizations.get.return_value = org
        mocker.patch("polar_cli.commands.org.set_default_org_id")

        result = runner.invoke(cli_app, ["org", "set-default", "org-1"])
        assert result.exit_code == 0
        assert "Default organization set" in result.output
