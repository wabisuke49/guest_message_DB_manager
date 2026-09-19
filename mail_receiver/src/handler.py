"""SMTP DATA handler with no persistence or message parsing responsibilities."""

from __future__ import annotations

import inspect
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

MessageCallback = Callable[[str, list[str], bytes], None | Awaitable[None]]


@dataclass(frozen=True)
class ReceivedMessage:
    """The SMTP envelope data made available to later application layers."""

    mail_from: str
    rcpt_tos: list[str]
    content: bytes


class SMTPReceiveHandler:
    """Accept SMTP messages and pass their unparsed bytes to an optional callback."""

    def __init__(self, on_message: MessageCallback | None = None) -> None:
        self._on_message = on_message
        self._logger = logging.getLogger(__name__)

    async def handle_DATA(self, _server: object, _session: object, envelope: object) -> str:
        """Receive an SMTP envelope and acknowledge it without storing its contents."""
        mail_from = str(envelope.mail_from)
        rcpt_tos = list(envelope.rcpt_tos)
        content = envelope.content
        if not isinstance(content, bytes):
            content = str(content).encode("utf-8")

        message = ReceivedMessage(mail_from=mail_from, rcpt_tos=rcpt_tos, content=content)
        try:
            if self._on_message is not None:
                result = self._on_message(message.mail_from, message.rcpt_tos, message.content)
                if inspect.isawaitable(result):
                    await result
        except Exception:
            # Do not allow a future downstream handler failure to terminate SMTP service.
            self._logger.exception("Unable to hand off received SMTP message")
            return "451 Requested action aborted: local error in processing"

        # Deliberately log metadata only; message headers and body may be sensitive.
        self._logger.info(
            "Accepted SMTP message: sender=%s recipients=%d size_bytes=%d",
            message.mail_from,
            len(message.rcpt_tos),
            len(message.content),
        )
        return "250 Message accepted for delivery"
