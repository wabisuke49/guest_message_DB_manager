# mail_receiver

`aiosmtpd` を利用した、メール保存・パースを行わない最小の SMTP 受信サーバーです。

## 起動

Python 3.10 以降で依存関係をインストールしてから起動します。

```bash
cd mail_receiver
python -m pip install -r requirements.txt
python main.py
```

デフォルトでは `0.0.0.0:1025` を待ち受けます。`SMTP_HOST` と `SMTP_PORT` で変更できます。

```bash
SMTP_HOST=127.0.0.1 SMTP_PORT=1026 python main.py
```

受信時には送信元、宛先数、原文バイト数のみをログへ出します。メール本文やヘッダーは出力しません。

## 動作確認

サーバー起動後、別ターミナルで実行します。

```bash
python - <<'PY'
import smtplib

with smtplib.SMTP("127.0.0.1", 1025) as client:
    client.sendmail(
        "sender@example.test",
        ["recipient@example.test"],
        b"Subject: SMTP receive test\r\n\r\nHello.\r\n",
    )
PY
```

SMTP クライアントは `250` を受け取ります。現時点ではメールを保存・パース・HTTP 送信しません。

## テスト

```bash
cd mail_receiver
python -m unittest discover -s tests -v
```
