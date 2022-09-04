from flask import Flask, request, abort

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

line_bot_api = LineBotApi('gcC8J+3w6NtzLWtGCpln4w4X1Yv7KBGUITmAVgsFkKNNAu5fOfK5T5NvcZJVK7c2Jm6rv4WlfakxNjGO9wNIe6AedtKYV5Na3p7zYELTWuHDdPg/5q7MxFvaTMrH1ZF1hxfZLrrZKuDa4/IDOz3rAQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dc4418683f507409ea90b5fdce144e27')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()