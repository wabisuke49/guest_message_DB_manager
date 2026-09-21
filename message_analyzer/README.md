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

## テスト

```bash
cd message_analyzer
python -m unittest discover -s tests
```
