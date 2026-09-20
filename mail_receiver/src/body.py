"""Utilities for extracting a decoded plain-text body from raw EML bytes."""

from email import policy
from email.parser import BytesParser


def extract_plain_text_body(eml_bytes: bytes) -> str | None:
    """Return the first ``text/plain`` body decoded from raw EML bytes.

    The email package decodes Content-Transfer-Encoding and the part charset.
    HTML fallback and attachment filtering are outside the MVP scope. Return
    ``None`` when no ``text/plain`` part exists.
    """
    message = BytesParser(policy=policy.default).parsebytes(eml_bytes)

    for part in message.walk():
        if part.get_content_type() != "text/plain":
            continue

        content = part.get_content()
        return content
