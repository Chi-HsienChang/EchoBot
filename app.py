from flask import Flask, request, abort
import requests
import json
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, MessagingApiBlob,
    ImageMessage, AudioMessage, VideoMessage,
    QuickReply, QuickReplyItem, ReplyMessageRequest,
    TextMessage, MessageAction, TemplateMessage,
    RichMenuSize, RichMenuRequest, RichMenuArea, RichMenuBounds,
    URIAction
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

def create_rich_menu_1():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        rich_menu = RichMenuRequest(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name="Rich Menu 2",
            chat_bar_text="想要學習的內容是?????",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=4, y=0, width=866, height=627),
                    action=MessageAction(type="message", text="Area 1")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=891, y=21, width=805, height=610),
                    action=MessageAction(type="message", text="Area 2")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1733, y=29, width=726, height=606),
                    action=MessageAction(type="message", text="Area 3")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=8, y=652, width=858, height=544),
                    action=URIAction(type="uri", uri="https://www.islam.org.hk/e19/")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=899, y=668, width=801, height=528),
                    action=MessageAction(type="message", text="Area 5")
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1749, y=664, width=718, height=536),
                    action=MessageAction(type="message", text="Area 6")
                )
            ]
        )

        response = line_bot_api.create_rich_menu(rich_menu_request=rich_menu)
        print(f"🎨 Rich Menu 已建立，ID: {response.rich_menu_id}")

        return response.rich_menu_id  # 回傳 Rich Menu ID

def upload_rich_menu_image(rich_menu_id):
    url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "image/png"
    }
    image_path = "static/test.png"

    with open(image_path, "rb") as image_file:
        response = requests.post(url, headers=headers, data=image_file.read())

    if response.status_code == 200:
        print("✅ Rich Menu 圖片上傳成功")
    else:
        print(f"❌ Rich Menu 圖片上傳失敗: {response.text}")

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
            QuickReplyItem(action=MessageAction(label="禮拜33333", text="禮拜")),
            QuickReplyItem(action=MessageAction(label="圖片", text="圖片")),
            QuickReplyItem(action=MessageAction(label="錄音", text="錄音")),
            QuickReplyItem(action=MessageAction(label="影片", text="影片")),
            QuickReplyItem(action=MessageAction(label="連結", text="連結")),
            QuickReplyItem(action=MessageAction(label="禮拜2", text="禮拜")),
            QuickReplyItem(action=MessageAction(label="圖片2", text="圖片")),
            QuickReplyItem(action=MessageAction(label="錄音2", text="錄音")),
            QuickReplyItem(action=MessageAction(label="影片2", text="影片")),
            QuickReplyItem(action=MessageAction(label="連結2", text="連結")),
            QuickReplyItem(action=MessageAction(label="禮拜3", text="禮拜")),
            QuickReplyItem(action=MessageAction(label="圖片3", text="圖片")),
            QuickReplyItem(action=MessageAction(label="如何成為穆斯林", text="如何成為穆斯林")),
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
        elif user_message == '禮拜了嗎?':
            messages = [TextMessage(text='準備去禮拜!', quick_reply=quick_reply_options)]
        elif user_message == '如何成為穆斯林':
            url = request.url_root + 'static/become_muslim.jpeg'
            messages = [
                ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="點擊連結\n\n預約會議: https://reurl.cc/XZKlxE")
            ]
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
    rich_menu_id = create_rich_menu_1()
    print("rich_menu_id=", rich_menu_id)
    upload_rich_menu_image(rich_menu_id)
    app.run(host="0.0.0.0", port=5001)
