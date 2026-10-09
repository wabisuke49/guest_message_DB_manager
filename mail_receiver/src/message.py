"""Build MVP message data from saved AirHost EML files."""

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .body import extract_plain_text_body


def get_message_data(eml_path: Path) -> dict[str, str | None]:
    """Return MVP message data extracted from one saved EML file."""
    body = extract_plain_text_body(eml_path.read_bytes())
    message_data = {
        "message_id": get_message_id(eml_path),
        "received_at": get_received_at(eml_path),
    }

    if body is None:
        return message_data | {
            "session_id": None,
            "house_id": None,
            "guest_message": None,
        }

    return message_data | extract_message_data(body)


def extract_message_data(body: str) -> dict[str, str | None]:
    """Return message fields extracted from a decoded email body."""
    guest_message = get_guestmessage(body)
    session_id = get_session_id(body)
    house_id = get_house_id(body)

    return {
        "session_id": session_id,
        "house_id": house_id,
        "guest_message": guest_message,
    }


def get_message_id(eml_path: Path) -> str:
    """Return the UUID filename of a saved EML as its message ID."""
    return eml_path.stem


def get_received_at(eml_path: Path) -> str:
    """Return the saved EML file's modified time as a UTC timestamp."""
    modified_at = datetime.fromtimestamp(eml_path.stat().st_mtime, timezone.utc)
    return modified_at.isoformat().replace("+00:00", "Z")


def get_guestmessage(body: str) -> str | None:
    """Return the guest message between the inquiry marker and detail URL."""

    MESSAGE_START = "からの問い合わせを確認してください："
    lines = body.splitlines()
    start_index = next(
        (index for index, line in enumerate(lines) if MESSAGE_START in line), None
    )

    detail_index = next(
        (
            index
            for index, line in enumerate(lines[start_index + 1:], start_index + 1)
            if line.startswith("詳細を見る:")
        ),
        None,
    )

    return "\n".join(lines[start_index + 1 : detail_index]).strip()

def get_session_id(body: str) -> str | None:
    """Return the session ID from the AirHost detail line."""
    for line in body.splitlines():
        if line.startswith("詳細を見る:"):
            query = urlparse(line.removeprefix("詳細を見る:").strip()).query
            params = parse_qs(query)
            return params.get("ticketId", [""])[0]

def get_house_id(body: str) -> str | None:
    """Return the house ID from the AirHost detail line."""
    for line in body.splitlines():
        if line.startswith("詳細を見る:"):
            query = urlparse(line.removeprefix("詳細を見る:").strip()).query
            params = parse_qs(query)
            return params.get("houseId", [""])[0]
