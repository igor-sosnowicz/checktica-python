"""Module with pytest fixtures accessible to all tests."""

import socket
from collections.abc import Generator

import pytest


@pytest.fixture
def disabled_internet_access() -> Generator[None]:
    """Fixture that disables Internet access during the execution of a test using it."""

    def guard(*args, **kwargs) -> None:
        raise ConnectionError("Cannot connect to the Internet.")

    original_socket = socket.socket
    try:
        socket.socket = guard
        yield
    finally:
        socket.socket = original_socket
