"""Tests for error handler decorator."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest
import typer
from polar_sdk.models import PolarError, SDKError

from polar_cli.errors import handle_errors


class TestHandleErrors:
    def test_passes_through_on_success(self):
        @handle_errors
        def ok():
            return 42

        assert ok() == 42

    def test_reraises_typer_exit(self):
        @handle_errors
        def exits():
            raise typer.Exit(0)

        with pytest.raises(typer.Exit):
            exits()

    def test_reraises_typer_abort(self):
        @handle_errors
        def aborts():
            raise typer.Abort()

        with pytest.raises(typer.Abort):
            aborts()

    def test_catches_sdk_error(self):
        @handle_errors
        def api_fail():
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 404
            resp.headers = httpx.Headers()
            raise SDKError("not found", resp, body='{"detail":"Not found"}')

        with pytest.raises(typer.Exit):
            api_fail()

    def test_catches_polar_error(self):
        @handle_errors
        def sdk_fail():
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 422
            resp.headers = httpx.Headers()
            raise PolarError("something broke", resp)

        with pytest.raises(typer.Exit):
            sdk_fail()

    def test_catches_connect_error(self):
        @handle_errors
        def conn_fail():
            raise httpx.ConnectError("connection refused")

        with pytest.raises(typer.Exit):
            conn_fail()

    def test_catches_timeout(self):
        @handle_errors
        def timeout_fail():
            raise httpx.ReadTimeout("read timed out")

        with pytest.raises(typer.Exit):
            timeout_fail()

    def test_catches_generic_exception(self):
        @handle_errors
        def generic_fail():
            raise ValueError("unexpected")

        with pytest.raises(typer.Exit):
            generic_fail()

    def test_preserves_function_name(self):
        @handle_errors
        def my_func():
            pass

        assert my_func.__name__ == "my_func"
