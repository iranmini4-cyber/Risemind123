import telebot
import os
from youtubesearchpython import VideosSearch
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# دکمه‌ها برای start
def start_buttons():
    markup = InlineKeyboardMarkup()
    # دکمه پیام به مدیر
    markup.add(InlineKeyboardButton("پیام دادن به من", url="https://t.me/MINYATOOOOR"))
    # دکمه افزودن به گروه
    markup.add(InlineKeyboardButton("اضافه کردن به گروه", url=f"https://t.me/{bot.get_me().username}?startgroup=true"))
    return markup

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "سلام 👋\nربات RiseMind فعال شد 🤖", reply_markup=start_buttons())

# /help
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "دستورات:\n/start\n/help\n/song [اسم آهنگ]", reply_markup=start_buttons())

# /song جستجوی دستی
@bot.message_handler(commands=['song'])
def song_search(message):
    try:
        query = message.text.replace("/song", "").strip()
        if not query:
            bot.reply_to(message, "لطفاً نام آهنگ را بعد از /song وارد کن.")
            return

        videosSearch = VideosSearch(query, limit=3)
        results = videosSearch.result()['result']

        reply = ""
        for i, video in enumerate(results, 1):
            reply += f"{i}. {video['title']}\n{video['link']}\n\n"

        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"خطا در جستجو: {e}")

# پیام گروه برای پخش آهنگ خودکار
@bot.message_handler(func=lambda message: True)
def auto_play(message):
    try:
        text = message.text.lower()
        if "play" in text or "پخش" in text:
            query = text.replace("play", "").replace("پخش", "").strip()
            if not query:
                bot.reply_to(message, "لطفاً نام آهنگ را بنویسید.")
                return

            videosSearch = VideosSearch(query, limit=3)
            results = videosSearch.result()['result']

            reply = f"نتایج جستجوی '{query}':\n\n"
            for i, video in enumerate(results, 1):
                reply += f"{i}. {video['title']}\n{video['link']}\n\n"

            bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"خطا در جستجو: {e}")

bot.infinity_polling()
