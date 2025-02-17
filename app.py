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
            QuickReplyItem(action=MessageAction(label="人生目標", text="人生目標")), #1
            QuickReplyItem(action=MessageAction(label="六大信仰", text="六大信仰")), #2
            QuickReplyItem(action=MessageAction(label="真主尊名", text="真主尊名")), #3
            QuickReplyItem(action=MessageAction(label="禮拜時間", text="禮拜時間")), #4
            QuickReplyItem(action=MessageAction(label="主麻聚禮", text="主麻聚禮")), #5
            QuickReplyItem(action=MessageAction(label="參觀清真寺", text="參觀清真寺")), #6
            QuickReplyItem(action=MessageAction(label="基礎課程", text="基礎課程")), #7
            QuickReplyItem(action=MessageAction(label="認識先知", text="認識先知")), #8  
            QuickReplyItem(action=MessageAction(label="聖訓學習", text="聖訓學習")), #9     
            QuickReplyItem(action=MessageAction(label="兩個節日", text="兩個節日")), #10
            QuickReplyItem(action=MessageAction(label="學習網站", text="學習網站")), #11
            QuickReplyItem(action=MessageAction(label="機構網站", text="機構網站")), #12
            QuickReplyItem(action=MessageAction(label="清真飲食", text="清真飲食")), #13
        ])

        if user_message == '人生目標':
            messages = [TextMessage(text='好的，以下是禮拜的資訊！', quick_reply=quick_reply_options)]
        elif user_message == '六大信仰':
            url = request.url_root + 'static/test.jpeg'
            messages = [ImageMessage(original_content_url=url, preview_image_url=url)]
        elif user_message == '真主尊名':
            messages = [TextMessage(text='真主尊名', quick_reply=quick_reply_options)]
        elif user_message == '禮拜時間':
            messages = [TextMessage(text='禮拜時間', quick_reply=quick_reply_options)]
        elif user_message == '主麻聚禮':
            messages = [TextMessage(text='主麻聚禮', quick_reply=quick_reply_options)]
        elif user_message == '參觀清真寺':
            url = request.url_root + 'static/mosque.jpeg'
            messages = [
                ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="✅ 點擊下方連結 ✅\n\n馬上預約: https://reurl.cc/NbKpAQ")
            ]
        elif user_message == '基礎課程':
            messages = [TextMessage(text='基礎課程', quick_reply=quick_reply_options)]
        elif user_message == '認識先知':
            messages = [TextMessage(text='認識先知', quick_reply=quick_reply_options)]
        elif user_message == '聖訓學習':
            messages = [TextMessage(text='聖訓學習', quick_reply=quick_reply_options)]
        elif user_message == '兩個節日':
            messages = [TextMessage(text='兩個節日', quick_reply=quick_reply_options)]
        elif user_message == '學習網站':
            url = 'https://www.islam.org.hk/e19/'
            messages = [TextMessage(text=f'這是伊斯蘭之光的網站:\n{url}', quick_reply=quick_reply_options)]
        elif user_message == '機構網站':
            url = 'https://www.islam.org.hk/'
            messages = [TextMessage(text=f'這是伊斯蘭之光的網站:\n{url}', quick_reply=quick_reply_options)]
        elif user_message == '清真飲食':
            url = 'https://www.islam.org.hk/e19/'
            messages = [TextMessage(text=f'這是伊斯蘭之光的網站:\n{url}', quick_reply=quick_reply_options)]
        #################################################
        #################################################
        #################################################
        elif user_message == '如何成為穆斯林':
            url = request.url_root + 'static/become_muslim.jpeg'
            messages = [
                ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="✅ 點擊下方連結 ✅\n\n預約會議: https://reurl.cc/XZKlxE")
            ]
        elif user_message == '如何禮拜':
            messages = [TextMessage(text="在學習禮拜前，需要先學習 **大淨** 與 **小淨**。\n\n因為穆斯林需要具有 **大淨與小淨** 才能禮拜。\n\n"
                                        "✅ **洗大淨方法**:\n(1) 舉意洗大淨。\n(2) 用水清洗**全身** 即可。\n\n"
                                        "✅ **洗小淨方法**:\n"
                                        "(1) **小淨的前提：淨下**\n"
                                        "    - 小淨前要先「淨下」，即清洗私密處。\n"
                                        "    - 穆斯林習慣用水清洗後，再用衛生紙擦拭。\n\n"
                                        "(2) **洗手三次** 🖐️\n"
                                        "(3) **漱口三次** 👄\n"
                                        "(4) **嗆鼻三次** 👃\n"
                                        "(5) **洗臉三次** 🧼\n"
                                        "(6) **洗手掌至手肘三次** ✋\n"
                                        "    - 先洗右手，再洗左手。\n"
                                        "(7) **抹頭** 💦\n"
                                        "(8) **洗腳三次** 🦶\n"
                                        "    - 先洗右腳再洗左腳。\n"
                                        "📅 **預約會議**: [點擊連結](https://reurl.cc/XZKlxE)")]
        elif user_message == '如何封齋':
            messages = [TextMessage(text='學習中文', quick_reply=quick_reply_options)]
        elif user_message == '如何天課':
            url = request.url_root + 'static/mosque.jpeg'
            messages = [
                ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="✅ 點擊下方連結 ✅\n\n馬上預約: https://reurl.cc/NbKpAQ")
            ]
        elif user_message == '如何朝覲':
            url = 'https://www.islam.org.hk/e19/'
            messages = [TextMessage(text=f'這是伊斯蘭之光的網站:\n{url}', quick_reply=quick_reply_options)]
        elif user_message == '古蘭經學習':
            url = 'https://www.islam.org.hk/'
            messages = [TextMessage(text=f'這是伊斯蘭之光的網站:\n{url}', quick_reply=quick_reply_options)]
        else:
            messages = [TextMessage(text='願真主賜您平安\n使用說明: \n', quick_reply=quick_reply_options)]
        


        # elif user_message == '影片':
        #     url = request.url_root + 'static/test.MOV'
        #     messages = [VideoMessage(original_content_url=url, preview_image_url=url)]
        # elif user_message == '連結':
        #     url = 'https://www.islam.org.hk/e19/'
        #     messages = [TextMessage(text=f'這是伊斯蘭之光的網站:\n{url}', quick_reply=quick_reply_options)]


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
