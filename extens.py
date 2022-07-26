import json
import requests
from conf import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f"Одинаковые валюты: перевод невозможен {base}!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать, измените количество {amount}!")

        r = requests.get(f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={base_key}&tsyms={sym_key}")
        resp = json.loads(r.content)
        new_price = resp[base_key][sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Количество {amount} {base} в {sym}: {new_price}"
        return message
