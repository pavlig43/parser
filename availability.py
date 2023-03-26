import json
import os


def availability(page, lst, tag_name):  # Добавляет 0 в значение, если оно отсутствует у карточки товара(цена,скидка и т.д)
    try:
        lst.append(page.find(tag_name[0], tag_name[1]).text)
    except:
        lst.append(0)

def my_choice_json(bolder_shop):
    with open(rf'C:\Users\user\PycharmProjects\parser\{bolder_shop}\my_choice.json', 'r') as file:
        my_choice = file.read()
    return json.loads(my_choice)
#if __name__ == '__main__':


