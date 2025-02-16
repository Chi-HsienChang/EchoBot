from flask import Flask, request, abort
import requests
import json
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ImageMessage, AudioMessage, VideoMessage,
    QuickReply, QuickReplyItem, ReplyMessageRequest,
    TextMessage, MessageAction
)
from linebot.v3.webhooks import MessageEvent, FollowEvent, TextMessageContent

import os

app = Flask(__name__)

# 你的 Line Bot 設定
configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@line_handler.add(FollowEvent)
def handle_follow(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text='願真主賜您平安')]
            )
        )

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text.strip()
    print(f"✅ 收到訊息: {user_message}")

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        quick_reply_options = QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="禮拜~~", text="禮拜")),
            QuickReplyItem(action=MessageAction(label="圖片", text="圖片")),
            QuickReplyItem(action=MessageAction(label="錄音", text="錄音")),
            QuickReplyItem(action=MessageAction(label="影片", text="影片")),
            QuickReplyItem(action=MessageAction(label="連結", text="連結")),
            QuickReplyItem(action=MessageAction(label="禮拜2", text="禮拜")),
            QuickReplyItem(action=MessageAction(label="圖片2", text="圖片")),
            QuickReplyItem(action=MessageAction(label="錄音2", text="錄音")),
            QuickReplyItem(action=MessageAction(label="影片2", text="影片")),
            QuickReplyItem(action=MessageAction(label="連結2", text="連結")),
            QuickReplyItem(action=MessageAction(label="錄音222", text="錄音")),
            QuickReplyItem(action=MessageAction(label="影片222", text="影片")),
            QuickReplyItem(action=MessageAction(label="連結13", text="連結"))
        ])

        if user_message == '禮拜':
            messages = [TextMessage(text='好的，以下是禮拜的資訊！', quick_reply=quick_reply_options)]
        elif user_message == '圖片':
            url = request.url_root + 'static/test.jpeg'
            messages = [ImageMessage(original_content_url=url, preview_image_url=url)]
        elif user_message == '錄音':
            url = request.url_root + 'static/test.m4a'
            messages = [AudioMessage(original_content_url=url, duration=10000)]
        elif user_message == '影片':
            url = request.url_root + 'static/test.MOV'
            messages = [VideoMessage(original_content_url=url, preview_image_url=url)]
        elif user_message == '連結':
            url = 'https://www.islam.org.hk/e19/'
            messages = [TextMessage(text=f'這是伊斯蘭之光的網站:\n{url}', quick_reply=quick_reply_options)]
        else:
            messages = [TextMessage(text='願真主賜您平安', quick_reply=quick_reply_options)]

        print(f"📤 準備回應: {messages}")

        try:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages
                )
            )
            print("✅ LINE API 回應成功")
        except Exception as e:
            print(f"❌ LINE API 發送失敗: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
