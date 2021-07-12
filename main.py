import os
import telebot
import re

from extensions import Curr

currencies = {
    'доллар': 'USD',
    'рубль': 'RUB',
    'биткоин': 'BTC',
}

bot = telebot.TeleBot(os.getenv('TEL_TOKEN'))


message_help = 'введите сообщение в формате <из какой валюты> <в какую валюту> <сумма>\n \
/values для получения списка доступных валют'


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Бот для пересчета из одной валюты в другую.\n\
{message_help}')


@bot.message_handler(commands=['values'])
def handle_start_help(message):
    m_text = 'доступные валюты:\n' + '\n'.join(currencies.keys())
    bot.send_message(message.chat.id, m_text)


@bot.message_handler(content_types=['text', ])
def convert(message):
    re_str = '^(\w+)\s+(\w+)\s+(\d+\.{0,1}\d*)$'
    match = re.match(re_str, message.text)
    if not match:
        bot.reply_to(message, message_help)
        return

    cur_from, cur_to, amount = match.groups()
    if not cur_from in currencies or not cur_to in currencies:
        bot.reply_to(message, message_help)
        return
    
    key_cur_from = currencies[cur_from]
    key_cur_to = currencies[cur_to]
    
    sum = Curr.get_price(key_cur_from, key_cur_to, amount)
    
    message_text = f'Цена {amount} {cur_to} в {cur_from} - {sum}'
    bot.reply_to(message, message_text)


bot.polling(none_stop=True)