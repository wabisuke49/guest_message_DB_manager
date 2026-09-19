"""Run the SMTP receiver."""

from threading import Event

from aiosmtpd.controller import Controller

from src.handler import SMTPReceiveHandler

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 1025


def main() -> None:
    host = str(DEFAULT_HOST)
    port = int(str(DEFAULT_PORT))
    controller = Controller(SMTPReceiveHandler(), hostname=host, port=port)

    controller.start()

    Event().wait()

if __name__ == "__main__":
    main()
