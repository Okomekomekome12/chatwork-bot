# chatwork-python

## はじめに
このコードはPythonでChatwork APIを簡単に使えるようにするだけの物です()
ただそれだけという()

## インストール・準備

### 必要なもの
- Python 3.x
- requests ライブラリ
- Chatwork APIトークン

### APIトークンの取得方法
1. Chatworkにログイン
2. 右上のアイコン → 「サービス連携」→ 「APIトークン」
3. 「新しいトークンを発行」をクリック

## 使い方
    messagesend    メッセージを送信
    viewer     閲覧者を決める
    admin      管理者を決める
    member     メンバーを決める
    member_remove メンバーを削除する
    get_new_messages 最新のメッセージを取得
    get_message_link 最新のメッセージのリンクを取得
    create_task タスクを作成する
    delete_task タスクを削除する

### 基本的な使い方

```python
import chatwork

# セットアップ
cw = chatwork.setup("ルームID", "APIトークン")

# メッセージ送信
cw.messagesend("Hello World")

cw.viewer("メンバーID")

cw.admin("メンバーID")

cw.member("メンバーID")

cw.member_remove("メンバーID")

messages1 = cw.get_new_messages()

print(messages1)

messagelink = cw.get_message_link()

print(messagelink)

cw.create_task("タスク内容","担当者")

task_id = cw.create_task("タスク内容","担当者")

print(task_id)

cw.delete_task("タスクid")