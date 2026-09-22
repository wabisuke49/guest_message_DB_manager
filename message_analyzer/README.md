# Message Analyzer

フェーズ2のゲストメッセージ受信・分析サービスです。Python 3.11以上を対象とします。

## ローカル起動

```bash
cd message_analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

起動後、次のリクエストで稼働を確認できます。

```bash
curl http://127.0.0.1:8000/health
```

レスポンス:

```json
{"status":"ok"}
```

## DB初期化

初回のみ、サーバーを起動する前に次のコマンドで `data/messages.db` を作成し、
`schema.sql` の初期スキーマを適用します。

```bash
cd message_analyzer
python -c "from database import initialize_database; initialize_database()"
```

## メッセージJSONの検証

`POST /messages` は、フェーズ1から受信するメッセージJSONを検証します。
この段階ではDBへ保存しません。

```bash
curl -X POST http://127.0.0.1:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "b76674b0-a19b-4aa9-9d15-09ac4cf31871",
    "received_at": "2026-09-22T10:00:00Z",
    "session_id": "3885c57d-28c0-4777-92e2-cd293c4cac08",
    "house_id": "01f92a4a-bc7c-4e2a-919d-02c4e9ac1b52",
    "guest_message": "チェックイン方法を教えてください。"
  }'
```

UUID、UTCのISO 8601日時（`Z` または `+00:00`）、空白以外の文字を含むメッセージを必須とします。成功時は `200 OK` と `{"status":"validated"}` を返します。

## DBスキーマの変更

初期スキーマは `schema.sql` で管理します。運用済みDBの構造を変更する場合は、
`migrations/001_説明.sql` のように連番と内容を含むSQLファイルを追加します。

migrationファイルの適用は自動化せず、変更内容を確認して明示的に実行します。運用が複雑になった場合に、SQLAlchemyとAlembicなどの導入を検討します。

## テスト

```bash
cd message_analyzer
python -m unittest discover -s tests -t . -v
```
