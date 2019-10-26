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

line_channel_secret = "61dfbc9f442a233e35131a84efaaeea5"
line_channel_access_token = "iaUI9wkTtTNBmqfwohvUJ6AOLRSnU++G4EFpz2TiI/PbguxfbKFQaVKpelnea02q09PdQfq7s4ECKAiGg8KGdFQT0jaHIcDuMkvXC244fzqg5JuW46I8N4/GKclfke49DwD7g81V/vCmgLk0J61vYgdB04t89/1O/w1cDnyilFU="

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
        "apikey": "DZZQUtEk52iIqcZh99dWlFz13zY2V2QU",
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
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port ] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)