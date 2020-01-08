# line_bot

## 概要
messanger APIとtalk apiをpythonで実装する。

<br>

## Procfile
Flask + gunicorn
プログラムの実行方法

<br>

## runtime.txt
自身のpythonのバージョン

<br>

## requirements.txt
必要なライブラリ

<br>

## app.py
ソースコード

```python
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
import urllib
import json
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_channel_secret = "*********************"
line_channel_access_token = "****************************"

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)


@app.route("/callback", methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    data = {
        "apikey": "*********************",
        "query": event.message.text ,
    }
 
    data = urllib.parse.urlencode(data).encode("utf-8")
    with urllib.request.urlopen("https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk", data=data) as res:

        reply_json = json.loads(res.read().decode("unicode_escape"))
        
        if reply_json['status'] == 0:
            reply = reply_json['results'][0]['reply']
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run()
```

<br>

## 詳細
```python
line_channel_secret = "*********************"
line_channel_access_token = "****************************"
```
      
自身のChannel Secret、アクセストークンを取得。
****

```python
@app.route("/callback", methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
```
       
X-Line-Signatureリクエストヘッダーをテキスト形式で取得し、webhookを操作する。
****

```python
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    data = {
        "apikey": "*********************",
        "query": event.message.text ,
    }
 
    data = urllib.parse.urlencode(data).encode("utf-8")
    with urllib.request.urlopen("https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk", data=data) as res:

        reply_json = json.loads(res.read().decode("unicode_escape"))
 
        if reply_json['status'] == 0:
            reply = reply_json['results'][0]['reply']
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply))
 ```
                    
talk apiにて、json形式の応答を返す。
apikeyは自身のキーを入力する。
****

```python
if __name__ == "__main__":
    app.run()
```
        
webサーバーの立ち上げを行う。
****

<br>

## 動作イメージ
