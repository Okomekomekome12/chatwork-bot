import time
import chatwork

def main():
    cw = chatwork.setup(423252546, "9f89821d6eac0bba7adb611b00fc164e")
    seen = set()

    while True:
        try:
            messages = cw.get_new_messages()

            # メッセージがない場合スキップ
            if not messages:
                time.sleep(3)
                continue

            # リスト全件をループ
            for msg in messages:
                mid = msg["message_id"]

                # 既読スキップ
                if mid in seen:
                    continue
                seen.add(mid)

                body = msg.get("body", "")
                print(f"送信者: {msg['account']['name']}")
                print(f"メッセージ: {body}")

                # 荒らし判定
                if body.count("(quick)") >= 10 or body.count(":*") >= 10:
                    cw.viewer(msg["account"]["account_id"])
                    cw.messagesend("[info][title]荒らし検知[/title]荒らしを検知しました、流します[/info]")
                    for i in range(29):
                        cw.messagesend("a")
                        time.sleep(0.6)
                    message_id = msg["message_id"]
                    mesagelink = f"https://www.chatwork.com/#!rid423252546-{message_id}"
                    cw.messagesend("[info][title]荒らし対処完了[/title]メッセージリンクを配布します[/info]")
                    cw.messagesend(f"[info][title]メッセリンク配布[/title]{mesagelink}[/info]")

        except Exception as e:
            print(f"エラー: {e}")

        time.sleep(3)

main()