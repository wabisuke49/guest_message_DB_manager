"""Request schemas for the message analysis service."""

import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator, Field


UTC_DATETIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$"
)


class MessageRequest(BaseModel):
    """A validated message received from Phase 1."""

    message_id: UUID
    received_at: datetime
    session_id: UUID
    house_id: UUID
    guest_message: str = Field(..., min_length=1)

    @field_validator("received_at", mode="before")
    def validate_received_at_is_utc(value) -> object:
        """Require an ISO 8601 UTC datetime with Z or +00:00."""
        if not isinstance(value, str) or not UTC_DATETIME_PATTERN.fullmatch(value):
            raise ValueError("received_at must be an ISO 8601 UTC datetime")

        return value

    @field_validator("guest_message")
    def validate_guest_message_is_not_blank(value: str) -> str:
        """Reject messages made up of whitespace without changing their value."""
        if not value.strip():
            raise ValueError("guest_message must not be blank")

        return value
