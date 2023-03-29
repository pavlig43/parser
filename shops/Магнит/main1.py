import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from availability import availability, get_bs4
from category import get_all_category
from classes import MyJson


def main(): # в куки буду передавать город и магазин
    my_choice = MyJson('Магнит', 'my_choice')
    my_choice_json = my_choice.read_my_choice()
    my_choice_json = '[]='.join([bit_url for key in my_choice_json for name,bit_url in my_choice_json[key].items()]) # получаю куски url для отбора

    names = []
    links = []
    prices = []
    sales = []
    notes = []


    url = f'https://magnit.ru/promo/?category[]={my_choice_json}'
    # ДОБАВИТЬ SESSION


    main_page_text = get_bs4(url)  # получаю bs4 основного сайта


    page_number = 1
    data = {
        'page': f'{page_number}',
        'FILTER': 'true',
        'SORT': '',
    }
    ua = UserAgent().random
    headers = {'User-Agent': ua}
    response = requests.session()
    response = response.post(url, cookies={'mg_geo_id': '1795'},
                             headers=headers, data=data)    # получаю bs4 сайта с выбранной категорией 1 страницы
    page = BeautifulSoup(response.text, "html.parser")

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
    return {'Магнит': magnit_df}


if __name__ == '__main__':
    print(main())
