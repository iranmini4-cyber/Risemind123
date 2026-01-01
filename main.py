import telebot
import os
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ===================== دکمه‌ها =====================
def start_buttons():
    markup = InlineKeyboardMarkup()
    # دکمه پیام به مدیر
    markup.add(InlineKeyboardButton("پیام دادن به من", url="https://t.me/MINYATOOOOR"))
    # دکمه افزودن به گروه
    markup.add(InlineKeyboardButton("اضافه کردن به گروه", url=f"https://t.me/{bot.get_me().username}?startgroup=true"))
    return markup

# ===================== /start =====================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "سلام 👋\nربات RiseMind فعال شد 🤖", reply_markup=start_buttons())

# ===================== /help =====================
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "دستورات:\n/start\n/help\n/song [اسم آهنگ]", reply_markup=start_buttons())

# ===================== جستجو در سایت ایرانی =====================
def search_navaak(query):
    try:
        url = f"https://navaak.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for item in soup.select("a.song-title")[:3]:  # ۳ نتیجه اول
            title = item.get_text(strip=True)
            link = item.get("href")
            if not link.startswith("http"):
                link = "https://navaak.com" + link
            results.append(f"{title}\n{link}")
        if not results:
            results.append("نتیجه‌ای پیدا نشد.")
        return results
    except Exception as e:
        return [f"خطا در جستجو در NAVAak: {e}"]

# ===================== جستجوی یوتیوب =====================
def search_youtube(query):
    try:
        videosSearch = VideosSearch(query, limit=3)
        results = videosSearch.result()['result']
        reply = []
        for video in results:
            reply.append(f"{video['title']}\n{video['link']}")
        if not reply:
            reply.append("نتیجه‌ای پیدا نشد.")
        return reply
    except Exception as e:
        return [f"خطا در جستجوی یوتیوب: {e}"]

# ===================== /song جستجوی دستی =====================
@bot.message_handler(commands=['song'])
def song_search(message):
    query = message.text.replace("/song", "").strip()
    if not query:
        bot.reply_to(message, "لطفاً نام آهنگ را بعد از /song وارد کن.")
        return

    reply = f"نتایج یوتیوب:\n"
    for r in search_youtube(query):
        reply += r + "\n\n"

    reply += f"نتایج NAVAak:\n"
    for r in search_navaak(query):
        reply += r + "\n\n"

    bot.reply_to(message, reply)

# ===================== پیام گروه برای پخش آهنگ خودکار =====================
@bot.message_handler(func=lambda message: True)
def auto_play(message):
    try:
        text = message.text.lower()
        if "play" in text or "پخش" in text:
            query = text.replace("play", "").replace("پخش", "").strip()
            if not query:
                bot.reply_to(message, "لطفاً نام آهنگ را بنویسید.")
                return

            reply = f"نتایج یوتیوب:\n"
            for r in search_youtube(query):
                reply += r + "\n\n"

            reply += f"نتایج NAVAak:\n"
            for r in search_navaak(query):
                reply += r + "\n\n"

            bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"خطا در جستجو: {e}")

# ===================== اجرای ربات =====================
bot.infinity_polling()
