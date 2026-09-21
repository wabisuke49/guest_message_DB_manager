"""Extract the MVP message data from a decoded AirHost email body."""

from urllib.parse import parse_qs, urlparse

def extract_message_data(
    body: str, message_id: str, received_at: str
) -> dict[str, str] | None:
    """Return MVP message data, or ``None`` when required fields are missing."""
    guest_message = get_guestmessage(body)
    session_id = get_session_id(body)
    house_id = get_house_id(body)

    return {
        "message_id": message_id,
        "received_at": received_at,
        "session_id": session_id,
        "house_id": house_id,
        "guest_message": guest_message,
    }


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



