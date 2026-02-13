"""Module with data models."""

from typing import Literal

from pydantic import BaseModel, Field


class DetectionResult(BaseModel):
    """Result of the LLM detection on a text."""

    is_llm_generated: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    remarks: str


DetectionMethod = Literal[
    "most_accurate", "more_accurate", "balanced", "fast", "fastest"
]
