"""Process a saved EML file and send its message data to Phase 2."""

from pathlib import Path

from .client import send_message_data
from .message import get_message_data
from .validator import validate_message_data


def process_eml(eml_path: Path) -> int | None:
    """Extract, validate, and send message data from one saved EML file."""
    message_data = get_message_data(eml_path)
    validated_data = validate_message_data(message_data)
    if validated_data is None:
        return None

    print(validated_data)

    return send_message_data(validated_data)
