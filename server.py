import os
import time
from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, PlainTextResponse
import chatwork

app = FastAPI()

API_TOKEN = os.environ.get("CHATWORK_API_TOKEN", "")
WEBHOOK_SECRET = os.environ.get("CHATWORK_WEBHOOK_SECRET", None)
MY_ACCOUNT_ID = os.environ.get("CHATWORK_MY_ACCOUNT_ID", None)


# ─── もともとの main() の処理をそのまま関数化 ───
def spam_action(room_id, account_id):
    cw = chatwork.setup(room_id, API_TOKEN)

    cw.viewer(account_id)
    cw.messagesend("[info][title]荒らし検知[/title]荒らしを検知しました、流します[/info]")

    for i in range(29):
        cw.messagesend("a")
        time.sleep(0.6)

    mesagelink = cw.get_message_link()
    cw.messagesend("[info][title]荒らし対処完了[/title]メッセージリンクを配布します[/info]")

    report = chatwork.setup(room_id, API_TOKEN)
    report.messagesend("[info][title]メッセリンク配布[/title]メッセージリンクを配布します[/info]")
    report.messagesend(f"{mesagelink}")


@app.get("/")
async def health():
    return PlainTextResponse("running")


@app.get("/callback")
async def verify():
    return PlainTextResponse("OK")


@app.post("/callback")
async def callback(
    request: Request,
    background_tasks: BackgroundTasks,
    x_chatworkwebhooksignature: str = Header(None),
):
    body_bytes = await request.body()

    # 署名検証
    if WEBHOOK_SECRET:
        if not chatwork.webhook_verify_signature(
            body_bytes, x_chatworkwebhooksignature, WEBHOOK_SECRET
        ):
            raise HTTPException(status_code=403, detail="invalid signature")

    data = await request.json()

    room_id = chatwork.webhook_get_roomid(data)
    message = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data)
    message_id = chatwork.webhook_get_message_id(data)

    print(f"[受信] room={room_id} from={account_id} msg={message}")

    # 自分自身は無視
    if MY_ACCOUNT_ID and str(account_id) == str(MY_ACCOUNT_ID):
        return JSONResponse({"status": "skipped"})

    # ─── もともとの判定ロジックそのまま ───
    if message and (message.count("(quick)") >= 10 or message.count(":*") >= 10):
        background_tasks.add_task(spam_action, str(room_id), str(account_id))

    return JSONResponse({"status": "ok"})