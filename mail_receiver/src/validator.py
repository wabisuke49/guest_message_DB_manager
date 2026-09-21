"""Validate message data before sending it to Phase 2."""

from collections.abc import Mapping
from datetime import datetime, timedelta
from uuid import UUID


REQUIRED_FIELDS = {
    "message_id",
    "received_at",
    "session_id",
    "house_id",
    "guest_message",
}


def validate_message_data(data: Mapping[str, object]) -> dict[str, str] | None:
    """Return sendable message data, or ``None`` when validation fails."""
    if set(data) != REQUIRED_FIELDS:
        return None

    message_id = data["message_id"]
    received_at = data["received_at"]
    session_id = data["session_id"]
    house_id = data["house_id"]
    guest_message = data["guest_message"]

    if not all(
        isinstance(value, str)
        for value in (message_id, received_at, session_id, house_id, guest_message)
    ):
        return None

    if not _are_uuids(message_id, session_id, house_id):
        return None
    if not _is_utc_datetime(received_at):
        return None
    if not guest_message.strip():
        return None

    return {
        "message_id": message_id,
        "received_at": received_at,
        "session_id": session_id,
        "house_id": house_id,
        "guest_message": guest_message,
    }


def _are_uuids(*values: str) -> bool:
    try:
        for value in values:
            UUID(value)
    except ValueError:
        return False

    return True


def _is_utc_datetime(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False

    return parsed.utcoffset() == timedelta(0)
