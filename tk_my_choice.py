import importlib
import importlib.util
import sys
from tkinter import *
import json
from tkinter import ttk
import os

from classes import CheckboxTreeview, MyJson
from availability import *









class Sales:
    def __init__(self, bolder_shop):
        self.bolder_shop = bolder_shop
        #self.module = importlib.import_module(f'shops.{self.bolder_shop}\category')  # из названия папки магазина импортирую модуль
        module = 'main1'
        spec = importlib.util.spec_from_file_location(module, rf'shops/{bolder_shop}' + "/main1.py")
        main1 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main1)
        self.get_all_category = main1.get_all_category
        self.main = main1.main
        self.get_lst_shops = main1.get_lst_shops
        #self.get_cokie = main1.get_cokie


    def get_json_category(self):
        my_choice = MyJson(self.bolder_shop, 'my_choice')  # получаю словарь с моим выбором из jsona
        my_choice_old = my_choice.read_my_choice()
        dict_shop = self.get_all_category()  # получаю словарь со ВСЕМИ категориями , полученные с сайта
        root = Tk()
        root.geometry('600x900')
        root.title('1313')  # имя магазина
        tree = CheckboxTreeview(root, columns='value')
        vert_scroll = ttk.Scrollbar(root, orient='vertical', command=tree.yview)  # ползунок вертикальный
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
            root.destroy()
        btn = Button(text="Получить мой список")

        btn.bind("<ButtonPress>", get_my_choice)  # событие при нажатии кнопки , получаю мой выбор
        checkbutton_var = BooleanVar()  # создаю логическую переменую и привязываю ее к Checkbutton ниже
        Checkbutton(root, text='Снять/выбрать всё', variable=checkbutton_var).pack(anchor='e')

        def checked_all():  # функция,которая проверяет состояние Checkbutton
            for id in tree.get_children():  # и ставит или снимает галочки везде
                if checkbutton_var.get():
                    tree.item_check(id)
                else:
                    tree.item_uncheck(id)

        checkbutton_var.trace('w', lambda *_: checked_all())  # метод trace при нажатии галочки,вызывает функцию выше
        tree.pack(anchor='w')
        btn.pack(anchor='w')
        root.mainloop()


if __name__ == '__main__':

    a = Sales('5Пятерочка')
    # x = a.main()
    # for name, pd in x.items():
    #     pd.to_excel('sf.xlsx', index=False)



    #print(a.bolder_shop)
