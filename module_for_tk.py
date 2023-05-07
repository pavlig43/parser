import importlib
import importlib.util
import sys
from tkinter import *
import json
from tkinter import ttk
import os
from tkinter.ttk import Combobox

from classes import CheckboxTreeview, MyJson
from availability import *


def get_json_category(root1,bolder_shop, dict_shop):
    my_choice = MyJson(bolder_shop, 'my_choice')  # получаю словарь с моим выбором из jsona
    my_choice_old = my_choice.read_my_choice()
    root_choice = Toplevel(root1)
    root_choice.geometry('600x900')
    root_choice.title(f'{bolder_shop}')  # имя магазина
    tree = CheckboxTreeview(root_choice, columns='value')
    vert_scroll = ttk.Scrollbar(root_choice, orient='vertical', command=tree.yview)  # ползунок вертикальный
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

    def get_my_choice():
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
        my_choice.write_my_choice(my_choice_new)  # сохраняю в файл свой выбор
        root_choice.destroy()

    btn = Button(root_choice, text="Получить мой список",command=get_my_choice)

    checkbutton_var = BooleanVar()  # создаю логическую переменую и привязываю ее к Checkbutton ниже
    Checkbutton(root_choice, text='Снять/выбрать всё', variable=checkbutton_var).pack(anchor='e')

    def checked_all():  # функция,которая проверяет состояние Checkbutton
        for id in tree.get_children():  # и ставит или снимает галочки везде
            if checkbutton_var.get():
                tree.item_check(id)
            else:
                tree.item_uncheck(id)

    checkbutton_var.trace('w', lambda *_: checked_all())  # метод trace при нажатии галочки,вызывает функцию выше
    tree.pack(anchor='w')
    btn.pack(anchor='w')


def city_listbox(root1, cities1,all_cities,bolder_shop):
    cookie_file =MyJson(bolder_shop,'cookie')

    root_city = Toplevel(root1)
    root_city.geometry("500x500")
    root_city.title('Выбери город')

    def filter_cities(*args):
        # Получаем текст, введенный пользователем
        text = city_entry.get()
        # Фильтруем список городов, оставляем только те, которые содержат это слово
        filtered_cities = [city for city in cities1 if text.lower() in city.lower()]
        # Обновляем список городов в Listbox
        city_listbox.delete(0, END)
        for city in filtered_cities:
            city_listbox.insert(END, city)

    def item_city(event):
        index = city_listbox.curselection()  # получаю индекс выбранного элемента
        item = city_listbox.get(index)  # ролучаю название города по индексу
        city_entry.delete(0, END)
        city_entry.insert(0, item)

    def get_cookie():
        city = city_entry.get()
        cookie = cookie_file.read_my_choice()
        # в куках меняю название города путем присвоению новому городу-ключу старых значений
        try:
            cookie[city] = cookie[cookie.keys()[0]]
        except TypeError:
            cookie[city] = None
        cookie = {city:cookie[city]}
        cookie_file.write_my_choice(cookie)
        try:
            combobox_shop(root1, all_cities, bolder_shop)
        except:
            root_city.destroy()
        finally:
            root_city.destroy()

    # Создаем виджеты Entry и Listbox
    city_entry = Entry(root_city, background='#999999')
    city_listbox = Listbox(root_city,width=50)
    btn = Button(root_city, text='Выбран', command=get_cookie)

    # Связываем ввод пользователя с обработчиком filter_cities
    city_entry.bind("<KeyRelease>", filter_cities)
    city_listbox.bind('<<ListboxSelect>>', item_city)
    # Размещаем виджеты на окне

    btn.pack()
    city_entry.pack(side=TOP)

    city_listbox.pack(side=TOP)


def combobox_shop(root1,all_cities,  bolder_shop):
    #функция создает выпадающий список из магазинов и сохраненяет
    #параметры куки в файл для дальнейшего использования
    cookie_file = MyJson(bolder_shop, 'cookie')
    cookie = cookie_file.read_my_choice()
    if bolder_shop == "Магнит":
        try:
            city = list(cookie.keys())[0]
        except:
            city = 'г.Москва, Москва'
        cookie_shops = all_cities[city][1]#список вариантов мвгазинов мвгнит



    else:
        try:
            city = list(cookie.keys())[0]
        except:
            city='Москва'
        cookie_shops = [i['address'] for i in all_cities[city]]


    root_shop = Toplevel(root1)
    root_shop.title("Выбери магазин")

    def get_shop(event):
        selections = shop_combobox.get()
        index_shop = cookie_shops.index(selections)
        if bolder_shop == "Магнит":
            cookie[city]= [all_cities[city][0],all_cities[city][1][index_shop]]
        else:
            shop = all_cities[city][index_shop]
            cookie[city] = shop
        cookie_file.write_my_choice(cookie)
        root_shop.destroy()


    shop_combobox = Combobox(root_shop, values=cookie_shops, width=50)
    shop_combobox.bind('<<ComboboxSelected>>',get_shop)

    shop_combobox.pack()

if __name__ == '__main__':

    dic = {"г.Новочебоксарск":[{"id": 13272, "address": "ст-ца Выселки, ул. Советская, 4", "shop_code": "35V5"}, {"id": 13272, "address": "ст-ца Выселки, ул. Ткаченко, 52", "shop_code": "S375"}, {"id": 13272, "address": "ст-ца Выселки, пер. Калинина", "shop_code": "34GU"}, {"id": 13272, "address": "ст-ца Выселки, ул. Лунева, 29К", "shop_code": "Q855"}]}



    root = Tk()
    btn = Button(root, text='21', command=lambda: combobox_shop(root,dic,'5Пятерочка'))
    btn.pack()

    root.mainloop()

    #os.system(r'C:\Users\user\PycharmProjects\parser\shops\5Пятерочка\main1.py')
