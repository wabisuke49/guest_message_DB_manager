"""Run the SMTP receiver."""

from __future__ import annotations

import logging
import os
import signal
from threading import Event

from aiosmtpd.controller import Controller

from src.handler import SMTPReceiveHandler

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 1025


def smtp_address_from_environment() -> tuple[str, int]:
    """Return the listen address, allowing safe local overrides."""
    host = os.getenv("SMTP_HOST", DEFAULT_HOST)
    port = int(os.getenv("SMTP_PORT", str(DEFAULT_PORT)))
    if not 0 < port < 65536:
        raise ValueError("SMTP_PORT must be between 1 and 65535")
    return host, port


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    host, port = smtp_address_from_environment()
    controller = Controller(SMTPReceiveHandler(), hostname=host, port=port)
    stopped = Event()

    def stop_server(signum: int, _frame: object) -> None:
        logger.info("Stopping SMTP receiver (signal=%s)", signum)
        stopped.set()

    signal.signal(signal.SIGINT, stop_server)
    signal.signal(signal.SIGTERM, stop_server)

    controller.start()
    logger.info("SMTP receiver listening on %s:%s", host, port)
    try:
        stopped.wait()
    finally:
        controller.stop()


if __name__ == "__main__":
    main()
