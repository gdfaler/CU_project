import json
import os

import telebot
from telebot import types


MINI_APP_URL = os.getenv("MINI_APP_URL", "https://gdfaler.pythonanywhere.com/")
BOT_TOKEN = "8589284379:AAE16fyggdA0p12iSmACUu0bSMa8WHSLS8c"

bot = telebot.TeleBot(BOT_TOKEN)


def _mini_app_keyboard() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Попасть в команду мечты", web_app=types.WebAppInfo(url=MINI_APP_URL)))
    return kb


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Привет! Нажми на кнопку ниже, чтобы найти команду / сотоварища мечты",
        reply_markup=_mini_app_keyboard(),
    )


@bot.message_handler(content_types=["web_app_data"])
def web_app_data_handler(message: types.Message):
    raw = getattr(message.web_app_data, "data", None)
    if not raw:
        bot.send_message(message.chat.id, "Пришли данные из Mini App, но они пустые.")
        return

    try:
        payload = json.loads(raw)
        pretty = json.dumps(payload, ensure_ascii=False, indent=2)
        bot.send_message(message.chat.id, f"Получил данные из Mini App:\n{pretty}")
    except Exception:
        bot.send_message(message.chat.id, f"Получил строку из Mini App:\n{raw}")


@bot.message_handler(content_types=["text"])
def text_handler(message: types.Message):
    if message.text and message.text.strip() == "/app":
        bot.send_message(message.chat.id,
            "Открывай приложение кнопкой ниже)",
            reply_markup=_mini_app_keyboard())
        return

    elif message.text and message.text.strip() == "/help":
        bot.send_message(
            message.chat.id,
            "Привет! Отправь /start - чтобы мы тебя поприветствовали, /app - чтобы открыть наше приложение)",
            reply_markup=_mini_app_keyboard())
        return

    bot.send_message(message.chat.id, "Неизвестная команда(((")