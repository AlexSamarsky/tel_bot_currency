import os
import telebot

from extensions import Currencies, ConvertExeption, ResponseException
from consts import currencies, message_help


bot = telebot.TeleBot(os.getenv('TEL_TOKEN'))


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Бот для пересчета из одной валюты в другую.\n{message_help}')


@bot.message_handler(commands=['values'])
def handle_start_help(message):
    m_text = 'доступные валюты:\n' + '\n'.join(currencies.keys())
    bot.send_message(message.chat.id, m_text)


@bot.message_handler(content_types=['text', ])
def convert(message):
    
    try:
        cur_from, cur_to, amount, sum = Currencies.get_price(message.text)
    except ConvertExeption as e:
        bot.reply_to(message, f'{e}\n{message_help}')
    except ResponseException as e:
        bot.reply_to(message, f'{e}')
    except Exception as e:
        bot.reply_to(message, f'{e}')
    else:
        message_text = f'Цена {amount} {cur_to} в {cur_from} - {sum}'
        bot.reply_to(message, message_text)


bot.polling(none_stop=True)