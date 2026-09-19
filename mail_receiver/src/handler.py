"""SMTP DATA handler with no persistence or message parsing responsibilities."""

class SMTPReceiveHandler:
    """Accept SMTP messages and pass their unparsed bytes to an optional callback."""

    async def handle_DATA(self, _server: object, _session: object, envelope: object) -> str:
        """Receive an SMTP envelope and acknowledge it without storing its contents."""
        mail_from = str(envelope.mail_from)
        rcpt_tos = list(envelope.rcpt_tos)
        content = bytes(envelope.content)
        print(f"Received message from: {mail_from}")
        print(f"Recipients: {rcpt_tos}")
        print(f"Message : {content}")

        return "250 Message accepted for delivery"
