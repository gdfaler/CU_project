import telebot

bot = telebot.TeleBot('8589284379:AAE16fyggdA0p12iSmACUu0bSMa8WHSLS8c')

@bot.message_handler(commands=["start"])
def start(m, res=False):
   bot.send_message(m.chat.id, 'Напиши мне что-нибудь')


@bot.message_handler(content_types=["text"])
def handle_text(message):
   bot.send_message(message.chat.id, 'Вы написали:' + message.text)
bot.polling(none_stop=True, interval=0)