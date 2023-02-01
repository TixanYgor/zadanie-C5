import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"
        headers = {
            "apikey": "U6e8QzYTeySxtsb7tjN0jbHiZf72tfLd"
        }
        r = requests.get(url, headers=headers)
        resp = json.loads(r.content)
        new_price = resp['result']
        return round(new_price, 3)
