
from pydantic import BaseModel, Field
from typing import Literal


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation: list[dict] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    status: Literal["answered", "not_found"]
    sources: list[str]
    confidence: float = Field(..., ge=0, le=1)
