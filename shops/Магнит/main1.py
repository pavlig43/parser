import json
import os
import re
from tkinter import *
from tkinter import ttk

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from availability import availability, get_bs4

from classes import MyJson, CheckboxTreeview
from module_for_tk import get_json_category

my_choice = MyJson('Магнит', 'my_choice')



def main():  # в куки буду передавать город и магазин
    my_choice_jsonR = my_choice.read_my_choice()
    my_choice_json = '&category[]='.join([bit_url for key in my_choice_jsonR for name, bit_url in
                                          my_choice_jsonR[key].items()])  # получаю куски url для отбора

    names = []
    links = []
    prices = []
    sales = []
    notes = []

    url = f'https://magnit.ru/promo/?category[]={my_choice_json}'

    # ДОБАВИТЬ SESSION

    page_number = 1
    cookies = {'mg_geo_id': '1795'}
    data = {
        'page': f'{page_number}',
        'FILTER': 'true',
        'SORT': '',
    }
    ua = UserAgent().random
    headers = {'User-Agent': ua}
    response = requests.session()
    response = response.post(url, cookies=cookies,
                             headers=headers, data=data)  # получаю bs4 сайта с выбранной категорией 1 страницы
    page = BeautifulSoup(response.text, "html.parser")
    with open('page.html', 'w', encoding="utf-8") as f:
        f.write(page.text)

    while page.find(class_="js-promo-number").get('value') != '0':

        all_products = page.find_all('a', {'class': 'card-sale card-sale_catalogue'})
        for good in all_products:
            availability(good, sales,
                         tag_name=('div', {'class': 'label label_sm label_magnit card-sale__discount'}))
            availability(good, names, tag_name=('div', {'class': 'card-sale__title'}))
            links.append(f'https://magnit.ru{good.get("href")}')
            availability(good, prices, tag_name=('div', {'class': 'label__price label__price_new'}))
            availability(good, notes, tag_name=('div', {'class': 'card-sale__header'}))
        page_number += 1
        data = {
            'page': f'{page_number}',
            'FILTER': 'true',
            'SORT': '',
        }
        response = requests.post(url, cookies={'mg_geo_id': '1795'},
                                 headers=headers, data=data)  # получаю bs4 сайта с выбранной категорией 1 страницы
        page = BeautifulSoup(response.text, "html.parser")

    for i in prices:
        try:
            i = float(str(i).replace('\n', ' ').strip().replace(' ', '.'))

        except ValueError:
            i = 0

    sales = [re.search('\d+', str(sale)).group() for sale in sales]

    magnit_df = pd.DataFrame({'Наименование': names,
                              'Ссылка': links,
                              'Цена': prices,
                              'Скидка': sales,
                              'Примечание': notes})

    magnit_df = magnit_df.sort_values(by='Скидка', ascending=False)
    print(magnit_df)
    return {'Магнит': magnit_df}


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
    dict_category= {'Магнит': dict_category}
    with open('all_category.json', 'w', encoding='utf-8') as f:
        dict_category = json.dumps(dict_category,ensure_ascii=False)
        f.write(dict_category)



def see_my_choice():
    my_choice_jsonR = my_choice.read_my_choice()
    see_my_choice = Toplevel(root)
    see_my_choice.title('Мой выбор')
    my_choice_json = (i for name, cat in my_choice_jsonR.items() for i in cat)
    lst = Listbox(see_my_choice)
    for i in my_choice_json:
        lst.insert(END,i)
    lst.pack()
    label = Label(root,text='')
    label.pack()
    btn  = Button(see_my_choice,text='OK',command=see_my_choice.destroy).pack()





if __name__ == '__main__':
    with open('all_category.json', 'r',encoding='utf-8') as f:
        dict_category = f.read()
        dict_category = json.loads(dict_category)


    root = Tk()
    root.title('Магнит')
    get_all_category()
    btn_see_my_choice = Button(root, text='Посмотреть мой выбор',command=see_my_choice).pack()
    btn_main = Button(root, text='Получить скидки моего выбора',command=main).pack()
    btn_choice = Button(root, text='Изменить мой выбор',command=lambda: get_json_category(root,'Магнит',dict_category)).pack()
    root.mainloop()


