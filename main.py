from typing import Coroutine
import requests
from bs4 import BeautifulSoup
import time

class Currency:
    URL = 'https://ru.investing.com/crypto/xrp/xrp-usd'
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
    current_converted_price = 0
    difference = 0.00001

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",","."))

    def get_currency_price(self):
        full_page = requests.get(self.URL, headers = self.HEADER)
        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("span", {"class": "arial_26 inlineblock pid-1118146-last"})
        return convert[0].text
    
    def get_result(self):
        return True
    
    def check_currency(self):
        currency = float(self.get_currency_price().replace(",","."))
        if currency >= self.current_converted_price + self.difference:
            self.total = "Курс вырос на 10 центов: " + str(currency)
            print(self.total)
            self.get_result()

        elif currency <= self.current_converted_price - self.difference:
            self.total = "Курс упал на 10 центов: " + str(currency)
            print(self.total)
            self.get_result()

        print(currency)
        time.sleep(10)
    
    def get_answer(self):
        return self.total