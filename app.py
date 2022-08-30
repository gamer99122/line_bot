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

line_bot_api = LineBotApi('l+UmE6jERJOFBJfJi+D3kMfrFWQ4W9SVknjjzcwQNWp0pXwIHnjl3z2THW28burxJm6rv4WlfakxNjGO9wNIe6AedtKYV5Na3p7zYELTWuGTDzN/ISrzIo6+zJdl8aXjlzgWq8OU6nmlUOj3eoYE1QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9701289ce5e48f02f9341e181544a694')


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