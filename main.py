import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام 👋\nربات RiseMind فعال شد 🤖")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "دستورات:\n/start\n/help")

bot.infinity_polling()
