"""
=============================================
                使い方
            Hello World例
        import chatwork
        cw = chatwork.setup("ルームid、APIトークン")
        cw.messagesend("hello world")

    機能一覧

    messagesend    メッセージを送信
    viewer     閲覧者を決める
    admin      管理者を決める
    member     メンバーを決める
    member_remove メンバーを削除する
    get_new_messages 最新のメッセージを取得
    get_message_link 最新のメッセージのリンクを取得
    create_task タスクを作成する
    delete_task タスクを削除する
    webhook_get_message()
    webhook_get_roomid()
    webhook_get_account_id()
    webhook_get_message_id()
    webhook_verify_signature()
=============================================

"""

import time
import requests
import hashlib
import hmac
import base64

# ================================================================
#  Webhook ヘルパー
# ================================================================

def webhook_get_message(data: dict):
    """Webhook ペイロードからメッセージ本文を返す"""
    return data.get("webhook_event", {}).get("body")

def webhook_get_roomid(data: dict):
    """Webhook ペイロードからルームIDを返す"""
    return data.get("webhook_event", {}).get("room_id")

def webhook_get_account_id(data: dict):
    """Webhook ペイロードから送信者の account_id を返す"""
    return data.get("webhook_event", {}).get("from_account_id")

def webhook_get_message_id(data: dict):
    """Webhook ペイロードからメッセージIDを返す"""
    return data.get("webhook_event", {}).get("message_id")

def webhook_verify_signature(body_bytes: bytes, signature_header: str, secret_token: str) -> bool:
    """署名を検証して True / False を返す"""
    if secret_token is None:
        return True
    if signature_header is None:
        return False
    expected = base64.b64encode(
        hmac.new(
            base64.b64decode(secret_token),
            body_bytes,
            hashlib.sha256,
        ).digest()
    ).decode()
    return hmac.compare_digest(expected, signature_header)

class setup:
    def __init__(self, room_id, api_token):
        self.room_id = room_id
        self.api_token = api_token

    def messagesend(self, message):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/messages"
        payload = {"body": message}
        headers = {"x-chatworktoken": self.api_token}
        
        response = requests.post(url, data=payload, headers=headers)
        print(response.text)

    def viewer(self, account_id):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/members"
        headers = {"x-chatworktoken": self.api_token}

        # 現在のメンバーを取得
        current_members = requests.get(url, headers=headers)
        members_data = current_members.json()

        # メンバーIDをリストに格納
        admin_ids = []
        member_ids = []
        readonly_ids = []
        #選別作業()
        for member in members_data:
            role = member["role"]
            if f"{member['account_id']}" == f"{account_id}":
                continue
            if role == "admin":
                admin_ids.append(str(member["account_id"]))
            elif role == "member":
                member_ids.append(str(member["account_id"]))
            elif role == "readonly":
                readonly_ids.append(str(member["account_id"]))
        readonly_ids.append(str(account_id))

        payload = {
            "members_admin_ids": ",".join(admin_ids),
            "members_member_ids": ",".join(member_ids),
            "members_readonly_ids": ",".join(readonly_ids)
        }

        response = requests.put(url, data=payload, headers=headers)
        print(response.text)
    def admin(self,account_id):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/members"
        headers = {"x-chatworktoken": self.api_token}

        # 現在のメンバーを取得
        current_members = requests.get(url, headers=headers)
        members_data = current_members.json()

        # 既存のメンバーIDをリストに格納
        admin_ids = []
        member_ids = []
        readonly_ids = []
        #選別作業()
        for member in members_data:
            role = member["role"]
            if f"{member['account_id']}" == f"{account_id}":
                continue
            elif role == "admin":
                admin_ids.append(str(member["account_id"]))
            elif role == "member":
                member_ids.append(str(member["account_id"]))
            elif role == "readonly":
                readonly_ids.append(str(member["account_id"]))
        admin_ids.append(str(account_id))

        payload = {
            "members_admin_ids": ",".join(admin_ids),
            "members_member_ids": ",".join(member_ids),
            "members_readonly_ids": ",".join(readonly_ids)
        }

        response = requests.put(url, data=payload, headers=headers)
        print(response.text)
    def member(self,account_id):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/members"
        headers = {"x-chatworktoken": self.api_token}

        # 現在のメンバーを取得
        current_members = requests.get(url, headers=headers)
        members_data = current_members.json()

        # 既存のメンバーIDをリストに格納
        admin_ids = []
        member_ids = []
        readonly_ids = []
        #選別作業()
        for member in members_data:
            role = member["role"]
            if f"{member['account_id']}" == f"{account_id}":
                continue
            elif role == "admin":
                admin_ids.append(str(member["account_id"]))
            elif role == "member":
                member_ids.append(str(member["account_id"]))
            elif role == "readonly":
                readonly_ids.append(str(member["account_id"]))
        member_ids.append(str(account_id))

        payload = {
            "members_admin_ids": ",".join(admin_ids),
            "members_member_ids": ",".join(member_ids),
            "members_readonly_ids": ",".join(readonly_ids)
        }

        response = requests.put(url, data=payload, headers=headers)
        print(response.text)
    def member_remove(self,account_id):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/members"
        headers = {"x-chatworktoken": self.api_token}
        # 現在のメンバーを取得
        
        current_members = requests.get(url, headers=headers)
        members_data = current_members.json()
        # メンバーIDをリストに格納
        admin_ids = []
        member_ids = []
        readonly_ids = []
        #選別作業
        for member in members_data:
            role = member["role"]
            if f"{member['account_id']}" == f"{account_id}":
                continue
            elif role == "admin":
                admin_ids.append(str(member["account_id"]))
            elif role == "member":
                member_ids.append(str(member["account_id"]))
            elif role == "readonly":
                readonly_ids.append(str(member["account_id"]))
        payload = {
            "members_admin_ids": ",".join(admin_ids),
            "members_member_ids": ",".join(member_ids),
            "members_readonly_ids": ",".join(readonly_ids)
        }
        response = requests.put(url, data=payload, headers=headers)
        print(response.text)
    def get_new_messages(self):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/messages"
        headers = {"x-chatworktoken": self.api_token}
        params = {"force": 1}

        response = requests.get(url, headers=headers, params=params)
        messages = response.json()

        # 最新のメッセージを取得(messages[-1]にすることで最新100件のところ最新1件のみ取得)
        latest = messages[-1]
        print(f"送信者: {latest['account']['name']}")
        print(f"メッセージ: {latest['body']}")
        return latest
    def get_message_link(self):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/messages"
        headers = {"x-chatworktoken": self.api_token}
        params = {"force": 1}

        response = requests.get(url, headers=headers, params=params)
        messages = response.json()

        latest = messages[-1]
        message_id = latest["message_id"]
        link = f"https://www.chatwork.com/#!rid{self.room_id}-{message_id}"
        print(f"最新メッセージリンク: {link}")
        return link
    def create_task(self, task,account_id):
        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/tasks"
        payload = {
            "limit_type": "none",
            "body": task,
            "to_ids": account_id
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "x-chatworktoken": self.api_token
        }
        response = requests.post(url, data=payload, headers=headers)
        print(response.text)
        #変数で指定されたときtask_idを返すようにする
        task_id = response.json()["task_ids"]
        return task_id
    def delete_task(self,task_id):

        url = f"https://api.chatwork.com/v2/rooms/{self.room_id}/tasks/{task_id}/status"

        payload = { "body": "done" }
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "x-chatworktoken": self.api_token
        }

        response = requests.put(url, data=payload, headers=headers)

        print(response.text)
#ーーーーーーーメインコードーーーーーーーーーーー
def main():
    cw = setup(423252546, "9f89821d6eac0bba7adb611b00fc164e")
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
            report = setup(423252546, "9f89821d6eac0bba7adb611b00fc164e")
            report.messagesend(f"[info][title]メッセリンク配布[/title]メッセージリンクを配布します[/info]")
            report.messagesend(f"{mesagelink}")
main()