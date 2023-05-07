import json
import os
import re
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from tkinter import *

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from availability import availability, get_bs4
from classes import MyJson
from module_for_tk import *
from selenium import webdriver


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
        return lst_shops


def main():

    url = 'https://5ka.ru/special_offers'
    ua = UserAgent().random
    headers = {'User-Agent': ua}
    cookie = ''
    # page_get = requests.get(url, headers=headers, cookies=cookies, timeout=5)
    # main_page = BeautifulSoup(page_get.text, "html.parser")
    # all_categories_soup =  main_page.find_all('li', class_='categories-item')
    # s = main_page.find_all('label', class_='radio-wrap')
    # a = [i.text.strip() for i in all_categories_soup]
    # # a = [i.get('value') for i in all_categories_soup]
    # print(len(all_categories_soup))




# получаю словарь всех категорий и записываю в файл раз в день
def get_all_category():
    options = Options()
    ua = UserAgent().random

    options.add_argument(f'user-agent={ua}')
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.get('https://5ka.ru/special_offers')
    driver.maximize_window()
    # нажимаю на любое есто экрана
    action = ActionChains(driver)
    action.move_by_offset(100, 100).click().perform()
    # закрыываю куки
    btn_cl = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/main/aside/div/div/div/button/div')))
    btn_cl.click()
    # кнопка,которая расскрывает список всех категорий
    btn_33 = WebDriverWait(driver, 100).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div/div[2]/main/div[1]/main/div/div/div[2]/aside/button/div')))
    time.sleep(5)

    btn_33.click()
    page = driver.page_source
    page = BeautifulSoup(page, 'html.parser')

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
    category_dict = json.dumps(category_dict, ensure_ascii=False)
    with open('all_category.json', 'w', encoding='utf-8') as f:
        f.write(category_dict)
    driver.quit()


# обновляет город и магазин
def update_lbl():
    window_show_shop = Toplevel(root)

    with open('cookie.json', 'r') as f:
        info_dict = json.load(f)
        city = list(info_dict.keys())[0]
        try:
            shop = info_dict[city]['address']
        except:
            shop = 'Empty Address'
        info = f'{city}\n{shop}'
    lbl_show_shop = Label(window_show_shop, text=info).pack()
    btn_show_shop = Button(window_show_shop, text='OK', command=window_show_shop.destroy).pack()
    # закрываю это окно спустя 3 секунды
    window_show_shop.after(2000, lambda: window_show_shop.destroy())


# смотрю мой выбор категорий из json файла
def see_my_choice():
    with open('my_choice.json', 'r') as f:
        my_choice_jsonR = f.read()
        my_choice_jsonR = json.loads(my_choice_jsonR)
    see_my_choice = Toplevel(root)
    see_my_choice.geometry('500x500')
    see_my_choice.title('Мой выбор')
    my_choice_json = (i for name, cat in my_choice_jsonR.items() for i in cat)
    lst = Listbox(see_my_choice, width=50, height=30)
    vert_scroll = ttk.Scrollbar(see_my_choice, orient='vertical', command=lst.yview)  # ползунок вертикальный
    vert_scroll.pack(side='right', fill='y')

    for i in my_choice_json:
        lst.insert(END, i)
    lst.pack()
    label = Label(root, text='')
    label.pack()
    btn = Button(see_my_choice, text='OK', command=see_my_choice.destroy).pack()


if __name__ == '__main__':

    with open('all_category.json', 'r', encoding='utf-8') as f:
        all_category = f.read()
        all_category = json.loads(all_category)

    root = Tk()
    cities = list(get_all_cities().keys())
    shops = get_all_cities()  # список всех параметров в файле dict_cookie_all....
    btn_show_shop = Button(root, text='Посмотреть мой магазин', command=update_lbl).pack()
    btn_choice_city = Button(root, text='Выбрать город/магазин',
                             command=lambda: city_listbox(root, cities, shops, '5Пятерочка'),
                             bg='#7fa3b0', fg='#ffffff').pack()
    btn_see_my_choice = Button(root, text='Посмотреть мой выбор', command=see_my_choice).pack()
    btn_choice = Button(root, text='Изменить мой выбор',
                        command=lambda: get_json_category(root, '5Пятерочка', all_category)).pack()

    root.mainloop()
