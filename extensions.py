import os
import re
import requests
import json
from consts import currencies

CUR_TOKEN = os.getenv('CUR_TOKEN')


class ConvertExeption(Exception):
    pass


class ResponseException(Exception):
    pass

class Currencies:
    pass
    
    @staticmethod
    def get_price(message_text):

        re_str = '^(\w+)\s+(\w+)\s+(\d+\.{0,1}\d*)$'
        match = re.match(re_str, message_text)
        if not match:
            raise ConvertExeption('Не корректная команда')

        cur_from, cur_to, amount = match.groups()
        if not cur_from in currencies or not cur_to in currencies:
            raise ConvertExeption('Не известные валюты')
        
        key_cur_from = currencies[cur_from]
        key_cur_to = currencies[cur_to]
        
        try:
            res = requests.get(f'https://min-api.cryptocompare.com/data/price\
?fsym={key_cur_from}&tsyms={key_cur_to}&api_key={CUR_TOKEN}')
            obj = json.loads(res.text)
        except:
            raise ResponseException('Не удалось получить данные с сайта по курсам валют')
        
        cur_value = obj[key_cur_to]
        
        return cur_from, cur_to, amount, cur_value * float(amount)


