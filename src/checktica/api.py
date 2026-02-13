"""Module with definition of core SDK functions."""

from datetime import timedelta
from http import HTTPStatus
from typing import Final, get_args

import httpx
from loguru import logger
from retrying import retry

from checktica.data_models import DetectionMethod, DetectionResult
from checktica.exceptions import (
    APIAccessError,
    InvalidArgumentError,
    InvalidResponseError,
    LimitExceededError,
)

_CHECKTICA_API_URL: Final = "https://api.checktica.com"
_API_VERSION: Final = 1
_DETECTION_ENDPOINT: Final = "/is_ai"
_TIMEOUT: Final = timedelta(seconds=30).total_seconds()


def _construct_detection_endpoint_url() -> str:
    return f"{_CHECKTICA_API_URL}/v{_API_VERSION}{_DETECTION_ENDPOINT}"


def detect(
    text: str,
    detection_method: DetectionMethod = "most_accurate",
) -> DetectionResult:
    """
    Detect if AI was used to generate a given text.

    Args:
        text (str): Text to be checked.
        detection_method (DetectionMethod, optional): Detection method used to evaluate
            the text. The faster methods tend to be less accurate. Defaults to
            "most_accurate", which is the recommended method.

    Raises:
        InvalidArgumentError: Raised if the `text` parameter is empty, the
            `detection_method` parameter is empty, or the `detection_method` value
            is not one of the supported detection methods.
        LimitExceededError: Raised when the API rate limit has been exceeded.
            This occurs when too many requests have been made in a given time period.
        InvalidResponseError: Raised when the API returns an unexpected response
            or when there is an error parsing the response data.

    Returns:
        DetectionResult: An object containing the detection results.
    """
    if not text:
        raise InvalidArgumentError("`text` parameter cannot be empty.")
    if not detection_method:
        raise InvalidArgumentError("`detection_method` parameter cannot be empty.")
    if detection_method not in get_args(DetectionMethod):
        legal_values = ", ".join(get_args(DetectionMethod))
        raise InvalidArgumentError(
            f"`detection_method` cannot take the following value: {detection_method}."
            f"The only allowed values are: {legal_values}."
        )

    return _handle_request(
        text=text,
        detection_method=detection_method,
        timeout_in_seconds=_TIMEOUT,
    )


def _should_retry_on_exception(exception: Exception) -> bool:
    """
    Determine if an exception should trigger a retry.

    Do not retry on LimitExceededError as it abuses API guidelines.
    """
    return not isinstance(exception, LimitExceededError)


@retry(
    stop_max_attempt_number=3,
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,  # Exponential backoff up to 10 seconds.
    retry_on_exception=_should_retry_on_exception,
)
def _handle_request(
    text: str, detection_method: DetectionMethod, timeout_in_seconds: float
) -> DetectionResult:
    try:
        response = httpx.post(
            url=_construct_detection_endpoint_url(),
            timeout=timeout_in_seconds,
            json={"text": text, "method": detection_method},
        )
    except (httpx.ConnectError, httpx.TimeoutException) as e:
        raise APIAccessError from e

    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        msg = response.json().get(
            "detail", "Rate limit has been exceeded. Try again later."
        )
        logger.exception(msg)
        raise LimitExceededError(msg)
    if response.status_code != HTTPStatus.OK:
        msg = "Unknown API error has occurred. Please, try again later."
        logger.exception(msg)
        raise InvalidResponseError(msg)

    try:
        json = response.json()
        return DetectionResult(
            is_llm_generated=json["is_llm_generated"],
            remarks=json["remarks"],
            confidence=json["confidence"],
        )
    except Exception as e:
        logger.exception(e)
        raise InvalidResponseError from e
