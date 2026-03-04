import os
import time
import chatwork
from flask import Flask, request, jsonify

app = Flask(__name__)

API_TOKEN = "9f89821d6eac0bba7adb611b00fc164e"
SECRET_TOKEN = None

@app.route("/", methods=["GET"])
def health():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN):
        return "invalid signature", 403
    data = request.json
    room_id    = chatwork.webhook_get_roomid(data) # type: ignore
    body       = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data) # type: ignore
    message_id = chatwork.webhook_get_message_id(data)

    print(f"ルームID: {room_id}")
    print(f"送信者ID: {account_id}")
    print(f"メッセージ: {body}")

    cw = chatwork.setup(room_id, API_TOKEN)

    if body and (body.count("(quick)") >= 10 or body.count(":*") >= 10):
        cw.viewer(account_id)
        print(type(account_id))
        print(account_id)
        cw.messagesend("[info][title]荒らし検知[/title]荒らしを検知しました、流します[/info]")
        for i in range(29):
            cw.messagesend("a")
            time.sleep(0.6)
        message_link = cw.get_message_link()
        cw.messagesend("[info][title]荒らし対処完了[/title]メッセージリンクを配布します[/info]")
        cw.messagesend(f"[info][title]メッセリンク配布[/title]{message_link}[/info]")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)