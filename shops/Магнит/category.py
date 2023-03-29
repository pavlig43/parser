import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from availability import get_bs4



def get_all_category():
    url = 'https://magnit.ru/promo'
    page = get_bs4(url)
    lst_category = page.find_all(class_='checkbox')
    dict_category = {}
    for number, i in enumerate(lst_category):
        try:
            name = i.text.replace('\n', '')
            bit_url = i.find(class_="checkbox__control", id=re.compile('cat_')).get('value').strip()

            dict_category[name] = bit_url
        except AttributeError:
            continue
    return {'Магнит': dict_category}  # добавить название магазина

# if __name__ == '__main__':
