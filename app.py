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

line_bot_api = LineBotApi('pqPyEuP2PgA4CDav5+mPrUJ9qnrjX3VsgBIMJKDkgrg2wR520omyFooJkIL7KgGih10pEqcLojEbjvusYbXtGobgGHH+FTWDNSLA8zyLxMmuAF2MqEN9JYd3cWuW3msG7WPZz7w4+AGRGJDpu89OugdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d7aafd79765e40d9530d54952306aafa')


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