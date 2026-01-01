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

# ===================== جستجوی یوتیوب =====================
def search_youtube(query):
    try:
        videosSearch = VideosSearch(query, limit=3)
        results = videosSearch.result()['result']
        reply = []
        for video in results:
            reply.append(f"{video['title']}\n{video['link']}")
        return reply
    except:
        return []

# ===================== جستجوی سایت ایرانی =====================
def search_site(url, query, selector, prefix=""):
    try:
        full_url = f"{url}{query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(full_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for item in soup.select(selector)[:3]:  # ۳ نتیجه اول
            title = item.get_text(strip=True)
            link = item.get("href")
            if not link.startswith("http"):
                link = prefix + link
            results.append(f"{title}\n{link}")
        return results
    except:
        return []

def search_aha(query):
    return search_site("https://aha.ng/search?q=", query, "a.song-title")

def search_musics_fa(query):
    return search_site("https://musics-fa.com/?s=", query, "h2.entry-title a")

def search_rozmusic(query):
    return search_site("https://rozmusic.com/?s=", query, "h2.post-title a")

def search_upmusics(query):
    return search_site("https://upmusics.com/category/single-tracks/?s=", query, "h2.entry-title a")

def search_resanejavan(query):
    return search_site("https://resanejavan.net/?s=", query, "h2.entry-title a")

# ===================== جستجوی آهنگ =====================
def search_all(query):
    results = []
    results += search_youtube(query)
    results += search_aha(query)
    results += search_musics_fa(query)
    results += search_rozmusic(query)
    results += search_upmusics(query)
    results += search_resanejavan(query)
    return results

# ===================== /song =====================
@bot.message_handler(commands=['song'])
def song_search(message):
    query = message.text.replace("/song", "").strip()
    if not query:
        bot.reply_to(message, "لطفاً نام آهنگ را بعد از /song وارد کن.")
        return
    all_results = search_all(query)
    if all_results:
        bot.reply_to(message, "\n\n".join(all_results))
    else:
        bot.reply_to(message, "جستجو کردم، همچین آهنگی پیدا نکردم.")

# ===================== auto_play =====================
@bot.message_handler(func=lambda message: True)
def auto_play(message):
    text = message.text.lower()
    if "play" in text or "پخش" in text:
        query = text.replace("play", "").replace("پخش", "").strip()
        if not query:
            bot.reply_to(message, "لطفاً نام آهنگ را بنویسید.")
            return
        all_results = search_all(query)
        if all_results:
            bot.reply_to(message, "\n\n".join(all_results))
        else:
            bot.reply_to(message, "جستجو کردم، همچین آهنگی پیدا نکردم.")

# ===================== اجرای ربات =====================
bot.infinity_polling()
