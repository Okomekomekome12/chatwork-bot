import chatwork
import time

cw = chatwork.setup(423252546, "9f89821d6eac0bba7adb611b00fc164e")
seen = set()

while True:
    try:
        msg = cw.get_new_messages()
    except:
        continue

    if msg["message_id"] in seen:
        continue
    seen.add(msg["message_id"])

    if msg["body"].count("(quick)") >= 10 or msg["body"].count(":*") >= 10:
        cw.viewer(msg["account"]["account_id"])
        cw.messagesend("[info][title]荒らし検知[/title]荒らしを検知しました、流します[/info]")
        for i in range(29):
            cw.messagesend("a")
            time.sleep(0.6)
        mesagelink = cw.get_message_link()
        cw.messagesend("[info][/title]荒らし対処完了[/title]メッセージリンクを配布します[/info]")
        report = chatwork.setup(423252546, "9f89821d6eac0bba7adb611b00fc164e")
        report.messagesend(f"[info][title]メッセリンク配布[/title]メッセージリンクを配布します[/info]")
        report.messagesend(f"{mesagelink}")
