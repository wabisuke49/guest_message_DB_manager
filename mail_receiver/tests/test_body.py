"""Tests for decoded plain-text body extraction."""

import base64
import unittest

from src.body import extract_plain_text_body


class ExtractPlainTextBodyTests(unittest.TestCase):
    def test_decodes_base64_plain_text_from_multipart_email(self) -> None:
        body = "ゲストからの問い合わせです。"
        encoded_body = base64.b64encode(body.encode("utf-8")).decode("ascii")
        eml = f"""MIME-Version: 1.0
Content-Type: multipart/alternative; boundary=boundary

--boundary
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: base64

{encoded_body}
--boundary
Content-Type: text/html; charset=utf-8

<p>HTML本文</p>
--boundary--
        """.encode("utf-8")

        self.assertEqual(extract_plain_text_body(eml), body)
