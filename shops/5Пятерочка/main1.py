import json
import os
import re

from tkinter import *

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from availability import availability, get_bs4
from classes import MyJson
from module_for_tk import *


def get_lst_shops():  # обновлять раз в месяц
    file_path = os.path.join(os.path.dirname(__file__), 'lst_shops.json')
    with open(file_path, 'w') as file:
        url = 'https://5ka.ru/api/v2/stores/?bbox=0.0,0.0,180.0,180.0'  # список всех магазинов
        response = requests.get(url)
        lst_shops = response.text[9:-2]
        file.write(lst_shops)
    with open(file_path, 'r+') as file:
        file.seek(0)  # для возврата указателя в начало файла, чтобы прочитать
        lst_shops = file.read()
        lst_shops = json.loads(lst_shops)

        dict_cookie = {}
        for i, item in enumerate(lst_shops['data']['features']):
            id = item['properties']['city_id']
            city_name = item['properties']['city_name']
            address = item['properties']['address']
            shop_code = item['sap_code']
            if f'{city_name}' not in dict_cookie:
                dict_cookie[f'{city_name}'] = []
            dict_cookie[f'{city_name}'].append({'id': id, 'address': address, 'shop_code': shop_code})
        dict_cookie = json.dumps(dict_cookie, ensure_ascii=False)
        file.seek(0)
        file_path = os.path.join(os.path.dirname(__file__), 'dict_cookie_all_shops.json')
        with open(file_path, 'w') as f:
            f.write(dict_cookie)


def get_all_cities():
    file_path = os.path.join(os.path.dirname(__file__), 'dict_cookie_all_shops.json')
    with open(file_path, 'r') as file:
        lst_shops = file.read()
        lst_shops = json.loads(lst_shops)
    cities = list(lst_shops.keys())
    return cities


def main():
    lst_shops = MyJson('5Пяторочка', 'lst_shops')
    lst_shops.w
    lst_shops.read_my_choice()
    url = 'https://5ka.ru/special_offers'
    # ua = UserAgent().random
    # headers = {'User-Agent': ua}
    # cookies = {'location_id': '13272',
    #            'location': '%7B%22id%22%3A13272%2C%22name%22%3A%22%D1%81%D1%82-%D1%86%D0%B0%20%D0%92%D1%8B%D1%81%D0%B5%D0%BB%D0%BA%D0%B8%22%2C%22type%22%3A%22city%22%2C%22new_loyalty_program%22%3Atrue%2C%22site_shops_count%22%3A4%2C%22region%22%3A%7B%22id%22%3A42%2C%22name%22%3A%22%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BA%D1%80%D0%B0%D0%B9%22%7D%2C%22isConfirmed%22%3Atrue%7D',
    #            'selectedStore': '%7B%22id%22%3A14249%2C%22sap_code%22%3A%22Q855%22%2C%22address%22%3A%22%D1%81%D1%82-%D1%86%D0%B0%20%D0%92%D1%8B%D1%81%D0%B5%D0%BB%D0%BA%D0%B8%2C%20%D1%83%D0%BB.%20%D0%9B%D1%83%D0%BD%D0%B5%D0%B2%D0%B0%2C%2029%D0%9A%22%2C%22work_start_time%22%3A%2208%3A00%3A00%22%2C%22work_end_time%22%3A%2222%3A00%3A00%22%2C%22is_24h%22%3Afalse%7D'}
    # page_get = requests.get(url, headers=headers, cookies=cookies, timeout=5)
    # main_page = BeautifulSoup(page_get.text, "html.parser")
    # all_categories_soup =  main_page.find_all('li', class_='categories-item')
    # s = main_page.find_all('label', class_='radio-wrap')
    # a = [i.text.strip() for i in all_categories_soup]
    # # a = [i.get('value') for i in all_categories_soup]
    # print(len(all_categories_soup))

    # number_category = [number_category.find('label', class_='radio-wrap').get('value') for number_category in all_categories_soup]
    # all_categories_dict = {category.find('label', class_ = 'radio-wrap').get('value'): category.text for category in all_categories_soup}


def get_all_category():
    url = 'https://5ka.ru/special_offers'
    page = get_bs4(url)
    # добавить реальный сайт
    # file_path = os.path.join(os.path.dirname(__file__), 'change.html')
    # with open(file_path, 'r',encoding='utf-8') as html:
    #     page_text = BeautifulSoup(html, 'html.parser')

    # html = open('change.html', 'r', encoding='utf-8')
    # page_text = BeautifulSoup(html, 'html.parser')
    category_dict = {}

    category_name = page.find_all('li', class_='categories-item')
    for category in category_name:
        name_of_category = category.find('h4').text.strip()
        # ищу имена сабкатегорийй в основных
        subcutegories_names = [i.text.strip() for i in category.find_all('label', class_='radio-wrap')]
        # ищу номер категорий в этих именах сабкатегорий
        subcutegories_values = [i.find('input').get('value') for i in category.find_all('label', class_='radio-wrap')]
        category_dict[name_of_category] = {value: sub_name for value, sub_name in
                                           zip(subcutegories_names, subcutegories_values)}
    return category_dict


if __name__ == '__main__':

    root = Tk()
    cities = get_all_cities()
    options = (root, cities,'5Пятерочка')
    btn = Button(root, text='Выбрать город', command=lambda: (city_listbox(*options),)).pack()

    root.mainloop()
