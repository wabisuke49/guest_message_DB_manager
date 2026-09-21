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

起動時に `data/messages.db` を作成し、`schema.sql` の初期スキーマを自動適用します。

## DBスキーマの変更

初期スキーマは `schema.sql` で管理します。運用済みDBの構造を変更する場合は、
`migrations/001_説明.sql` のように連番と内容を含むSQLファイルを追加します。

migrationファイルの適用は自動化せず、変更内容を確認して明示的に実行します。運用が複雑になった場合に、SQLAlchemyとAlembicなどの導入を検討します。

## テスト

```bash
cd message_analyzer
python -m unittest discover -s tests -t . -v
```
