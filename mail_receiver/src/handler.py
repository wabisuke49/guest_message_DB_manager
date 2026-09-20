"""SMTP DATA handler that saves received messages as raw .eml files."""

from pathlib import Path
from uuid import uuid4


EML_DIRECTORY = Path(__file__).resolve().parent.parent / "data" / "eml"

class SMTPReceiveHandler:
    """Accept SMTP messages and save their unparsed bytes."""

    async def handle_DATA(self, _server: object, _session: object, envelope: object) -> str:
        """Save an SMTP envelope as an .eml file before acknowledging receipt."""
        content = bytes(envelope.content)

        try:
            EML_DIRECTORY.mkdir(parents=True, exist_ok=True)
            (EML_DIRECTORY / f"{uuid4()}.eml").write_bytes(content)
        except OSError:
            return "451 Requested action aborted: local error in processing"

        return "250 Message accepted for delivery"
