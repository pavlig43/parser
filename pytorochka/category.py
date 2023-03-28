import json

from bs4 import BeautifulSoup
import os

def get_all_category():
    # добавить реальный сайт
    file_path = os.path.join(os.path.dirname(__file__), 'change.html')
    with open(file_path, 'r',encoding='utf-8') as html:
        page_text = BeautifulSoup(html, 'html.parser')

    # html = open('change.html', 'r', encoding='utf-8')
    # page_text = BeautifulSoup(html, 'html.parser')
    category_dict = {}

    category_name = page_text.find_all('li', class_='categories-item')
    for category in category_name:
        name_of_category = category.find('h4').text.strip()
        # ищу имена сабкатегорийй в основных
        subcutegories_names = [i.text.strip() for i in category.find_all('label', class_='radio-wrap')]
        # ищу номер категорий в этих именах сабкатегорий
        subcutegories_values = [i.find('input').get('value') for i in category.find_all('label', class_='radio-wrap')]
        category_dict[name_of_category] = {value: sub_name for value, sub_name in zip(subcutegories_names, subcutegories_values)}
    return category_dict


if __name__ == '__main__':
    html = open('change.html', 'r', encoding='utf-8')
    print(get_all_category())


