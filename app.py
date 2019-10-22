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

# get channel_secret and channel_access_token from your environment variable
channel_secret = "61dfbc9f442a233e35131a84efaaeea5"
channel_access_token = "iaUI9wkTtTNBmqfwohvUJ6AOLRSnU++G4EFpz2TiI/PbguxfbKFQaVKpelnea02q09PdQfq7s4ECKAiGg8KGdFQT0jaHIcDuMkvXC244fzqg5JuW46I8N4/GKclfke49DwD7g81V/vCmgLk0J61vYgdB04t89/1O/w1cDnyilFU="
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
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
        #response = res.read().decode("utf-8")
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

    app.run(debug=options.debug, port=options.port