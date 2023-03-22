import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from availability import availability


def pyaterka():
    url = 'https://5ka.ru/special_offers'
    ua = UserAgent().random
    headers = {'User-Agent': ua}
    cookies = {'location_id': '13272',
               'location': '%7B%22id%22%3A13272%2C%22name%22%3A%22%D1%81%D1%82-%D1%86%D0%B0%20%D0%92%D1%8B%D1%81%D0%B5%D0%BB%D0%BA%D0%B8%22%2C%22type%22%3A%22city%22%2C%22new_loyalty_program%22%3Atrue%2C%22site_shops_count%22%3A4%2C%22region%22%3A%7B%22id%22%3A42%2C%22name%22%3A%22%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BA%D1%80%D0%B0%D0%B9%22%7D%2C%22isConfirmed%22%3Atrue%7D',
               'selectedStore': '%7B%22id%22%3A14249%2C%22sap_code%22%3A%22Q855%22%2C%22address%22%3A%22%D1%81%D1%82-%D1%86%D0%B0%20%D0%92%D1%8B%D1%81%D0%B5%D0%BB%D0%BA%D0%B8%2C%20%D1%83%D0%BB.%20%D0%9B%D1%83%D0%BD%D0%B5%D0%B2%D0%B0%2C%2029%D0%9A%22%2C%22work_start_time%22%3A%2208%3A00%3A00%22%2C%22work_end_time%22%3A%2222%3A00%3A00%22%2C%22is_24h%22%3Afalse%7D'}
    page_get = requests.get(url, headers=headers, cookies=cookies, timeout=5)
    main_page = BeautifulSoup(page_get.text, "html.parser")
    all_categories_soup =  main_page.find_all('li', class_='categories-item')
    s = main_page.find_all('label', class_='radio-wrap')
    a = [i.text.strip() for i in all_categories_soup]
    # a = [i.get('value') for i in all_categories_soup]
    print(len(all_categories_soup))

    # number_category = [number_category.find('label', class_='radio-wrap').get('value') for number_category in all_categories_soup]
    # all_categories_dict = {category.find('label', class_ = 'radio-wrap').get('value'): category.text for category in all_categories_soup}


if __name__ == '__main__':
    pyaterka()