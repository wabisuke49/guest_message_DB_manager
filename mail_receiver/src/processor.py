"""Process a saved EML file and send its message data to Phase 2."""

from datetime import datetime, timezone
from pathlib import Path

from .body import extract_plain_text_body
from .client import send_message_data
from .message import extract_message_data
from .validator import validate_message_data


def process_eml(eml_path: Path) -> int | None:
    """Extract, validate, and send message data from one saved EML file."""
    body = extract_plain_text_body(eml_path.read_bytes())
    if body is None:
        return None

    message_data = extract_message_data(
        body,
        message_id=eml_path.stem,
        received_at=_get_received_at(eml_path),
    )
    validated_data = validate_message_data(message_data)
    if validated_data is None:
        return None

    print(validated_data)

    return send_message_data(validated_data)


def _get_received_at(eml_path: Path) -> str:
    """Return the saved EML file's modified time as a UTC timestamp."""
    modified_at = datetime.fromtimestamp(eml_path.stat().st_mtime, timezone.utc)
    return modified_at.isoformat().replace("+00:00", "Z")
