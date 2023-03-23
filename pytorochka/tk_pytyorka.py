from tkinter import *
import json
from tkinter import ttk

from class_CheckBox import CheckboxTreeview
from category import get_all_category


def tk_category():
    old_men = {'олег': '35', 'паша': '30', 'вася': '25', 'коля': '20', 'жора': '15', 'макс': '10'}
    # men = {'олег':'35','паша':'30','вася':'25','коля':'20'}
    # men_json_str = json.dumps(men, ensure_ascii=False) # с русским текстом
    # with open('men.json','w') as file:
    # 	file.write(men_json_str)
    with open('men.json', 'r') as file:
        men_str = file.read()
    men = json.loads(men_str)

    def saved():
        new_dict = {}
        for key, value in old_men.items():
            if var_dict[key].get() == True:
                new_dict[key] = value
        print(new_dict)
        men_json_str = json.dumps(new_dict, ensure_ascii=False)  # с русским текстом
        with open('men.json', 'w') as file:
            file.write(men_json_str)
        root.destroy()

    # root = tk.Tk()
    # var_dict = {}
    # for i, (key, value) in enumerate(old_men.items()):
    #     if key in men:
    #         var_dict[key] = tk.BooleanVar(value=True)
    #     else:
    #         var_dict[key] = tk.BooleanVar()
    #     tk.Checkbutton(root, text=key, variable=var_dict[key]).grid(row=i, column=0)
    # tk.Button(root, text='SAVE', command=saved).grid(row=len(old_men))
    # root.mainloop()


def get_json_category(dict_shop):# передаю словарь с категориями , полученные с сайта
    root = Tk()
    root.geometry('600x900')
    root.title('1313')  # имя магазина
    tree = CheckboxTreeview(root, columns='value')
    vert_scroll = ttk.Scrollbar(root, orient='vertical', command=tree.yview)# ползунок вертикальный
    vert_scroll.pack(side='right', fill='y')
    tree.configure(height=40, yscrollcommand=vert_scroll.set)
    with open('my_choice.json', 'r') as file:# выгружаю из файла мой выбор
        my_choice = file.read()
    my_choice = json.loads(my_choice)

    for category in dict_shop:

        category_row = tree.insert("", 1, text=category)  # основные категории
        for sub_name, value in dict_shop[category].items():
            id2 = tree.insert(category_row, "end", text=sub_name, values=value)
            if category in my_choice.keys():
                if sub_name in my_choice[category]:  # проверка категорий с сайта на наличие в моем выборе
                    tree.item_check(id2) #ставлю галочки
                else:
                    tree.item_uncheck(id2)

    def get_my_choice(event):
		#функция при нажатии кнопки получить остатки
		#собирает все галочки и делает словарь и обновляет json с моим выбором
        my_choice = {}
        categories = tree.get_children()# список всех категорий в виджете
        for category in categories:
            subcategories = {}
            for subcategory in tree.get_children(category): # ищу подкатегори
                if 	tree.item(subcategory)['tags'] == ['checked']:
                    name = tree.item(subcategory)['text']  # имя , которое видит пользователь
                    value = tree.item(subcategory)['values'] # значение, которое к нему идет в словарь , используется для парсинга
                    subcategories[name] = str(value[0])

                    my_choice[tree.item(category)['text']] = subcategories #основной словарь дополняю словарем подкатегории
        my_choice_str = json.dumps(my_choice, ensure_ascii=False) # с русским текстом
        with open('my_choice.json','w') as file:
            file.write(my_choice_str)

    btn = Button(text="Получить мой список")

    btn.bind("<ButtonPress>", get_my_choice)# событие при нажатии кнопки , получаю мой выбор
    checkbutton_var = BooleanVar() # создаю логическую переменую и привязываю ее к Checkbutton ниже
    Checkbutton(root, text='Снять/выбрать всё', variable=checkbutton_var).pack(anchor='e')
    def checked_all():                  # функция,которая проверяет состояние Checkbutton
        for id in tree.get_children():  # и ставит или снимает галочки везде
            if checkbutton_var.get():
                tree.item_check(id)
            else:
                tree.item_uncheck(id)
    checkbutton_var.trace('w',lambda *_:checked_all()) #метод trace при нажатии галочки,вызывает функцию выше
    tree.pack(anchor='e')
    btn.pack(anchor='e')
    root.mainloop()



if __name__ == '__main__':
    a = get_all_category()

    get_json_category(a)
