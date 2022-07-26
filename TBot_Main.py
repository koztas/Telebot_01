import telebot
from extens import APIException, Converter
from conf import TOKEN, exchanges
import traceback

# exchanges = {
#     'доллар': 'USD',
#     'евро': 'EUR',
#     'рубль': 'RUB'
# }
# TOKEN = "5399199770:AAFCZzZdXnJ4I7-aSrJRGNMw5z4D78w3G3M"


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет, бро!"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException("Неверное количество параметров!")

        answer = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка написания команды:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
