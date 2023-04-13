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
    print(url)
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
    print({'Магнит': magnit_df})
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
    return {'Магнит': dict_category}


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
def get_json_category():
    dict_shop = get_all_category()
    my_choice_old =  my_choice.read_my_choice()
    root1 = Toplevel(root)
    root1.geometry('600x900')
    root1.title('Магнит')  # имя магазина
    tree = CheckboxTreeview(root1, columns='value')
    vert_scroll = ttk.Scrollbar(root1, orient='vertical', command=tree.yview)  # ползунок вертикальный
    vert_scroll.pack(side='right', fill='y')
    tree.configure(height=40, yscrollcommand=vert_scroll.set)

    for category in dict_shop:

        category_row = tree.insert("", 1, text=category)  # основные категории
        for sub_name, value in dict_shop[category].items():
            id2 = tree.insert(category_row, "end", text=sub_name, values=value)
            if category in my_choice_old.keys():
                if sub_name in my_choice_old[category]:  # проверка категорий с сайта на наличие в моем выборе
                    tree.item_check(id2)  # ставлю галочки
                else:
                    tree.item_uncheck(id2)

    def get_my_choice(event):
        # функция при нажатии кнопки получить остатки
        # собирает все галочки и делает словарь и обновляет json с моим выбором
        my_choice_new = {}
        categories = tree.get_children()  # список всех категорий в виджете
        for category in categories:
            subcategories = {}
            for subcategory in tree.get_children(category):  # ищу подкатегори
                if tree.item(subcategory)['tags'] == ['checked']:
                    name = tree.item(subcategory)['text']  # имя , которое видит пользователь
                    value = tree.item(subcategory)[
                        'values']  # значение, которое к нему идет в словарь , используется для парсинга
                    subcategories[name] = str(value[0])

                    my_choice_new[
                        tree.item(category)[
                            'text']] = subcategories  # основной словарь дополняю словарем подкатегории
        my_choice.write_my_choice(my_choice_new) # сохраняю в файл свой выбор
        root1.destroy()
    btn = Button(root1,text="Получить мой список")

    btn.bind("<ButtonPress>", get_my_choice)  # событие при нажатии кнопки , получаю мой выбор
    checkbutton_var = BooleanVar()  # создаю логическую переменую и привязываю ее к Checkbutton ниже
    Checkbutton(root1, text='Снять/выбрать всё', variable=checkbutton_var).pack(anchor='e')

    def checked_all():  # функция,которая проверяет состояние Checkbutton
        for id in tree.get_children():  # и ставит или снимает галочки везде
            if checkbutton_var.get():
                tree.item_check(id)
            else:
                tree.item_uncheck(id)

    checkbutton_var.trace('w', lambda *_: checked_all())  # метод trace при нажатии галочки,вызывает функцию выше
    tree.pack(anchor='w')
    btn.pack(anchor='w')




if __name__ == '__main__':
    main()
    root = Tk()
    btn_see_my_choice = Button(root, text='Посмотреть мой выбор',command=see_my_choice).pack()
    btn_main = Button(root, text='Получить скидки моего выбора',command=main).pack()
    btn_choice = Button(root, text='Изменить мой выбор',command=get_json_category).pack()
    root.mainloop()

