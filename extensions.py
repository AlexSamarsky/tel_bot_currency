import os
import requests
import json

CUR_TOKEN = os.getenv('CUR_TOKEN')

class Curr:
    pass
    
    @staticmethod
    def get_price(base, quote, amount):
        res = requests.get(f'https://min-api.cryptocompare.com/data/price\
?fsym={quote}&tsyms={base}&api_key={CUR_TOKEN}')
        obj = json.loads(res.text)
        cur_value = obj[base]
        return cur_value * float(amount)
