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
            messages = [TextMessage(
                text="📌 穆斯林的人生目標\n\n"
                    "1️⃣ 只崇拜唯一的真主\n"
                    "✅ 《古蘭經》指出：「我創造精靈與人類，只為讓他們崇拜我。」（51:56）\n"
                    "✅ 穆斯林透過禮拜、齋戒、誦讀《古蘭經》等方式來表達對真主的崇拜與感謝。\n\n"
                    "2️⃣ 成為受真主喜悅的穆斯林\n"
                    "✅ 人生以古蘭經和聖訓為指導，努力成為受真主喜悅的穆斯林。\n\n"
                    "3️⃣ 為永恆的後世做準備\n"
                    "✅ 在後世，每個人都將因其在短暫今世的行為而接受審判，最終只有兩種結果：進入天堂或墜入火獄。\n"
                    "✅ 先知穆罕默德（願主賜他平安）說：「當一個人去世後，他的一切善行都將終止，唯有三件事能使他持續獲得真主的報賞：對社會有益的施捨；留給後人的有益知識；以及為他虔誠祈禱的子女。」\n", quick_reply=quick_reply_options)]
        elif user_message == '六大信仰':
            messages = [
                TextMessage(text="信真主、信天使、信經典、信使者、信末日、信前定\n\n✅ 六大信仰介紹:\nhttps://reurl.cc/kMKlv9", quick_reply=quick_reply_options)]
    
        elif user_message == '真主尊名':
            messages = [
                TextMessage(text="真主的九十九個尊名:\nhttps://www.islamtaiwan.com/99-names", quick_reply=quick_reply_options)]
        elif user_message == '禮拜時間':
            messages = [
                TextMessage(text="台灣禮拜時間:\nhttps://www.islamtaiwan.com/", quick_reply=quick_reply_options)]
        elif user_message == '主麻聚禮':
            messages = [
                TextMessage(text="星期五主麻介紹:\nhttps://reurl.cc/V0b8lA", quick_reply=quick_reply_options)]
        elif user_message == '參觀清真寺':
            url = request.url_root + 'static/mosque.jpeg'
            messages = [
                ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="✅ 點擊下方連結 ✅\n\n馬上預約: https://reurl.cc/NbKpAQ", quick_reply=quick_reply_options)]
        elif user_message == '基礎課程':
            messages = [
                TextMessage(text="新穆斯林基礎課程\n\n✅ 共有8個影片:\n https://reurl.cc/NbKGaQ", quick_reply=quick_reply_options)]
        elif user_message == '認識先知':
            messages = [
                TextMessage(text="✅ 認識先知:\nhttps://reurl.cc/nqG7dl\n\n ✅ 先知穆罕默德:\nhttps://reurl.cc/d147j8", quick_reply=quick_reply_options)]
        elif user_message == '聖訓學習':
            messages = [
                TextMessage(text="✅ 聖訓學習:\nhttps://www.norislam.com/html/hadith/\n\n✅ 聖訓查詢:\nhttps://www.islam.org.hk/Bukhari_Online/bukhari_online_tc.aspx", quick_reply=quick_reply_options)]
        elif user_message == '兩個節日':
            messages = [TextMessage(text='每年的二次會禮（Eid Prayer）：\n\n 1️⃣ 開齋節會禮（Eid Al-Fitr） 回曆的九月為齋月，整個月裡日出至日落禁食。接著十月一日便可開齋，並舉行會禮，慶祝齋戒的完成，男女皆可至清真寺參加。 \n\n 2️⃣ 宰牲節會禮（Eid Al-Adha）（又稱犧牲節，忠孝節） 為回曆十二月十日，以紀念易布拉欣聖人及其子易斯瑪義對真主的絕對服從。會禮後如能力許可，應每人（或每戶）宰一隻羊，三分之一自家享用；三分之一給親友鄰居；三分之一給窮人。', quick_reply=quick_reply_options)]
        elif user_message == '學習網站':
            messages = [
                TextMessage(text="✅ 穆民基礎:\nhttps://www.islamtaiwan.com/muslim-basics\n\n✅ 穆民手冊:\nhttps://reurl.cc/74zke1", quick_reply=quick_reply_options)]
        elif user_message == '機構網站':
            messages = [
                TextMessage(text="✅ 台北清真寺:\nhttps://www.taipeimosque.org.tw/\n 台北清真寺FB:\nhttps://www.facebook.com/taipeimosque\n\n✅ 中國回教協會:\nhttps://www.cmainroc.org.tw/hot_cg22960.html\n中國回教協會FB:\n https://www.facebook.com/cmainroc\n\n✅ 財團法人中國回教文化教育基金會:\nhttps://ciceftw.org/\n 財團法人中國回教文化教育基金會FB:\nhttps://reurl.cc/Eg5o6m\n\n ✅ 以及更多伊斯蘭機構資訊:\n https://www.islamtaiwan.com/organizations", quick_reply=quick_reply_options)]
        elif user_message == '清真飲食':
            messages = [
                TextMessage(text="全台各地穆斯林友善餐廳、商店、以及住宿:\nhttps://www.islamtaiwan.com/halal", quick_reply=quick_reply_options)]
        #################################################
        elif user_message == '如何成為穆斯林':
            url = request.url_root + 'static/become_muslim.jpeg'
            messages = [
                ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="✅ 點擊下方連結 ✅\n\n預約會議: https://reurl.cc/XZKlxE")
            ]
        elif user_message == '如何禮拜':
            url = request.url_root + 'static/wash.jpeg'
            url2 = request.url_root + 'static/pray.jpeg'
            messages = [ImageMessage(original_content_url=url, preview_image_url=url),
                        ImageMessage(original_content_url=url, preview_image_url=url2),
                        TextMessage(text="穆斯林需要具有大淨與小淨\n才能禮拜。\n\n"

                                        "✅ 小淨教學:\n"
                                        "小淨影片教學之一:\nhttps://reurl.cc/NbKGaQ\n"
                                        "小淨影片教學之二:\nhttps://reurl.cc/46Vp2v\n\n" 

                                        "✅ 禮拜方法:\n"
                                        "每天五次禮拜:\nhttps://reurl.cc/oVEZy3\n" 
                                        "禮拜影片教學之ㄧ:\nhttps://reurl.cc/Eg5XG1\n" 
                                        "禮拜影片教學之二:\nhttps://reurl.cc/04M6Z6"
                                        )]
        elif user_message == '如何封齋':
            url = request.url_root + 'static/old_fasting.jpeg'
            messages = [
                ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="此照片為舊資訊\n2025年發布後會更新為最新版\n\n✅ 齋戒介紹:\nhttps://reurl.cc/96m1LO \n\n✅ 齋戒知識100問:\nhttps://reurl.cc/qnWZWN")
            ]
        elif user_message == '如何天課':
            # url = request.url_root + 'static/mosque.jpeg'
            messages = [
                # ImageMessage(original_content_url=url, preview_image_url=url),
                TextMessage(text="天課介紹:\nhttps://reurl.cc/M6KXEk")
            ]
        elif user_message == '如何朝覲':
            messages = [
                TextMessage(text="朝覲介紹:\nhttps://reurl.cc/eGKWNL")
            ]
        elif user_message == '古蘭經學習':
            messages = [
                TextMessage(text="✅ 學習網站:\nhttps://www.islamtaiwan.com/quran \n\n✅ 如何使用線上古蘭經:\nhttps://reurl.cc/qnWZER\n\n✅ 古蘭經講解115部影片:\nhttps://reurl.cc/WAKD4O" )
            ]
        else:
            messages = [TextMessage(
                text="願真主賜您平安\n\n"
                    "📌使用說明\n"
                    "請輸入以下關鍵字，獲取資訊：\n\n"
                    "🔹 如何成為穆斯林\n"
                    "🔹 如何禮拜\n"
                    "🔹 如何封齋\n"
                    "🔹 如何天課\n"
                    "🔹 如何朝覲\n"
                    "🔹 古蘭經學習\n\n"
                    "🔹 人生目標\n"
                    "🔹 六大信仰\n"
                    "🔹 真主尊名\n"
                    "🔹 禮拜時間\n"
                    "🔹 主麻聚禮\n"
                    "🔹 參觀清真寺\n\n"
                    "🔹 基礎課程\n"
                    "🔹 認識先知\n"
                    "🔹 聖訓學習\n"
                    "🔹 兩個節日\n"
                    "🔹 學習網站\n"
                    "🔹 機構網站\n"
                    "🔹 清真飲食\n\n"
                    "謝謝您😊"
            )]

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
