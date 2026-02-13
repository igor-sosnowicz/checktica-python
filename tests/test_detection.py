"""Module for testing detection method."""

import httpx
import pytest

from checktica import detect
from checktica.exceptions import APIAccessError, CheckticaError, LimitExceededError


@pytest.mark.parametrize(
    ("text", "method", "is_valid"),
    [
        (
            "This is a short but possible text to be checked.",
            "most_accurate",
            True,
        ),
        ("This is a short but possible text to be checked.", "more_accurate", True),
        ("This is a short but possible text to be checked.", "balanced", True),
        ("This is a short but possible text to be checked.", "fast", True),
        ("This is a short but possible text to be checked.", "fastest", True),
        (
            "This test case depends on sending a very, very long text ." * 60,
            "fastest",
            True,
        ),
        ("So short, so acceptable...", "most_accurate", True),
        ("", "most_accurate", False),  # Empty text
        ("This is a short but possible text to be checked", "", False),  # Empty method
        ("", "", False),  # Both text and method are empty.
        ("This is a short but possible text.", "NON-EXISTENT METHOD", False),
        ("", "NON-EXISTENT METHOD", False),  # Non-existent method and empty text
    ],
)
def test_detection(
    text: str,
    method: str,
    *,
    is_valid: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if detection succeeds given all parameters are valid and fail otherwise."""
    response = {"is_llm_generated": False, "remarks": "None.", "confidence": 0.75}

    def get_mocked_response(*args, **kwargs) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json=response,
        )

    monkeypatch.setattr(httpx, "post", get_mocked_response)

    if is_valid:
        detect(text=text, detection_method=method)  # pyright: ignore[reportArgumentType]
    else:
        with pytest.raises(CheckticaError):
            detect(text=text, detection_method=method)  # pyright: ignore[reportArgumentType]


def test_detection_without_connection(disabled_internet_access: None) -> None:
    """Test if a proper exception is rasied when there is no Internet connection."""
    text, method = "This is a short but possible text to be checked.", "most_accurate"

    with pytest.raises(APIAccessError):
        detect(text=text, detection_method=method)


def test_hitting_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test hitting a rate limit of the Checktica API."""

    def get_mocked_response_429(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status_code=429, json={"detail": "Rate limit exceeded"})

    def get_mocked_response_200(*args, **kwargs) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={"is_llm_generated": False, "remarks": "None.", "confidence": 0.75},
        )

    text, method = "This is a short but possible text to be checked.", "most_accurate"

    monkeypatch.setattr(httpx, "post", get_mocked_response_200)
    detect(text=text, detection_method=method)

    monkeypatch.setattr(httpx, "post", get_mocked_response_429)
    with pytest.raises(LimitExceededError):
        detect(text=text, detection_method=method)


def test_connection_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that APIAccessError is raised when request times out."""

    def mock_post_timeout(*args, **kwargs) -> None:
        raise httpx.TimeoutException("Request timed out")

    monkeypatch.setattr(httpx, "post", mock_post_timeout)

    text, method = "This is a short but possible text to be checked.", "most_accurate"
    with pytest.raises(APIAccessError):
        detect(text=text, detection_method=method)


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 500, 502, 503])
def test_various_http_errors(monkeypatch: pytest.MonkeyPatch, status_code: int) -> None:
    """Test that InvalidResponseError is raised for various HTTP error codes."""

    def mock_post_error(*args, **kwargs) -> httpx.Response:
        return httpx.Response(status_code=status_code, json={})

    monkeypatch.setattr(httpx, "post", mock_post_error)

    text, method = "This is a short but possible text to be checked.", "most_accurate"
    with pytest.raises(CheckticaError):
        detect(text=text, detection_method=method)


def test_malformed_json_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that InvalidResponseError is raised when response JSON is malformed."""

    def mock_post_malformed(*args, **kwargs) -> httpx.Response:
        # Missing required fields in JSON
        return httpx.Response(status_code=200, json={"is_llm_generated": True})

    monkeypatch.setattr(httpx, "post", mock_post_malformed)

    text, method = "This is a short but possible text to be checked.", "most_accurate"
    with pytest.raises(CheckticaError):
        detect(text=text, detection_method=method)
