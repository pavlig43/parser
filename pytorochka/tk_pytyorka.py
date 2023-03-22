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


def see_category(dict_shop):
    root = Tk()
    root.geometry('600x900')
    root.title('1313')  # имя магазина
    tree = CheckboxTreeview(root, columns='value')
    vert_scroll = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    vert_scroll.pack(side='right', fill='y')
    tree.configure(height=40, yscrollcommand=vert_scroll.set)
    men = {}

    for category in dict_shop:

        category_row = tree.insert("", 1, text=category)  # основные категории
        for sub_name, value in dict_shop[category].items():
            id2 = tree.insert(category_row, "end", text=sub_name, values=value)
            if sub_name in men:  # проверка на наличие вмоем выборе
                tree.item_check(id2)
            else:
                tree.item_uncheck(id2)

    def entered(event):
        my_choice = {}
        categories = tree.get_children()# список всех категорий в виджете
        for category in categories:
            subcategories = {}
            for subcategory in tree.get_children(category): # ищу подкатегории
                name = tree.item(subcategory)['text']  # имя , которое видит пользователь
                value = tree.item(subcategory)['values'] # значение, которое к нему идет в словарь , используется для парсинга

            subcategories[name] = str(value[0])

            my_choice[tree.item(category)['text']] = subcategories #основной словарь дополняю словарем подкатегории

        my_lst = tree.get_checked()
        # my_lst = [tree.item(i)['text'] for i in my_lst]
        my_lst1 = [tree.item(i)['values'] for i in my_lst]
        print(my_lst1)

    btn = Button(text="Entered")

    btn.bind("<ButtonPress>", entered)

    tree.pack()
    btn.pack()
    root.mainloop()


if __name__ == '__main__':
    a = get_all_category()

    see_category(a)
