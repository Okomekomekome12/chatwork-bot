"""
Render にデプロイする Chatwork Webhook 受信サーバー (FastAPI)

環境変数（Render の Dashboard → Environment で設定）
  CHATWORK_API_TOKEN      : Chatwork API トークン
  CHATWORK_WEBHOOK_SECRET : Webhook 署名トークン（任意）

Start Command（Render の Settings）:
  uvicorn server:app --host 0.0.0.0 --port $PORT
"""

import os
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import chatwork

app = FastAPI()

API_TOKEN      = os.environ.get("CHATWORK_API_TOKEN", "")
WEBHOOK_SECRET = os.environ.get("CHATWORK_WEBHOOK_SECRET", None)


# ─── ヘルスチェック（Render が生存確認に使う） ───
@app.get("/")
async def health():
    return PlainTextResponse("running")


# ─── Webhook URL 検証用 GET ───
@app.get("/callback")
async def verify():
    return PlainTextResponse("OK")


# ─── メッセージ受信 POST ───
@app.post("/callback")
async def callback(
    request: Request,
    x_chatworkwebhooksignature: str = Header(None),
):
    body_bytes = await request.body()

    # --- 署名検証 ---
    if not chatwork.webhook_verify_signature(
        body_bytes,
        x_chatworkwebhooksignature,
        WEBHOOK_SECRET,
    ):
        raise HTTPException(status_code=403, detail="invalid signature")

    data = await request.json()

    # --- Webhook ヘルパーでデータ取得 ---
    room_id    = chatwork.webhook_get_roomid(data)
    message    = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data)
    message_id = chatwork.webhook_get_message_id(data)

    print(f"[受信] room={room_id} from={account_id} msg={message}")

    # =============================================
    #  ★ ここに好きな処理を書く ★
    # =============================================
    #
    #  例1: オウム返し
    #  if room_id and message:
    #      cw = chatwork.setup(room_id, API_TOKEN)
    #      cw.messagesend(f"受信: {message}")
    #
    #  例2: 特定キーワードに反応
    #  if message and "ping" in message:
    #      cw = chatwork.setup(room_id, API_TOKEN)
    #      cw.messagesend("pong!")
    #
    # =============================================

    return JSONResponse({"status": "ok"})