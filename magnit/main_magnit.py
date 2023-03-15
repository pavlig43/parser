import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from availability import availability
from choice_category import choice_category


def get_bs4(url):

    ua = UserAgent().random
    headers = {'User-Agent': ua}

    page_get = requests.get(url, headers=headers, cookies={'mg_geo_id': '1795'})

    page = BeautifulSoup(page_get.text, 'html.parser')
    return page


def magnit():
    names = []
    links = []
    prices = []
    sales = []
    names_kosm = []
    links_kosm = []
    prices_kosm = []
    sales_kosm = []

    url = 'https://magnit.ru/promo'
    # ДОБАВИТЬ SESSION



    main_page_text = get_bs4(url)  # получаю bs4 основного сайта
    url = choice_category(main_page_text)
    page_number = 1
    data = {
        'page': f'{page_number}',
        'FILTER': 'true',
        'SORT': '',
    }
    ua = UserAgent().random
    headers = {'User-Agent': ua}

    response = requests.post(url, cookies={'mg_geo_id': '1795'},
                             headers=headers, data=data)    # получаю bs4 сайта с выбранной категорией 1 страницы
    page = BeautifulSoup(response.text, "html.parser")

    while page.find(class_="js-promo-number").get('value') != '0':

        all_products = page.find_all('a', {'class': 'card-sale card-sale_catalogue'})
        for good in all_products:
            if good.find('div', {'class': 'label label_sm label_magnit card-sale__discount'}):
                availability(good, sales,
                             tag_name=('div', {'class': 'label label_sm label_magnit card-sale__discount'}))
                availability(good, names, tag_name=('div', {'class': 'card-sale__title'}))
                links.append(f'https://magnit.ru{good.get("href")}')
                availability(good, prices, tag_name=('div', {'class': 'label__price label__price_new'}))
            else:
                availability(good, sales_kosm,
                             tag_name=('div', {'class': 'label label_sm label_cosmetic card-sale__discount'}))
                availability(good, names_kosm, tag_name=('div', {'class': 'card-sale__title'}))
                links_kosm.append(f'https://magnit.ru{good.get("href")}')
                availability(good, prices_kosm, tag_name=('div', {'class': 'label__price label__price_new'}))
        page_number += 1
        data = {
            'page': f'{page_number}',
            'FILTER': 'true',
            'SORT': '',
        }
        response = requests.post(url, cookies={'mg_geo_id': '1795'},
                                 headers=headers, data=data)  # получаю bs4 сайта с выбранной категорией 1 страницы
        page = BeautifulSoup(response.text, "html.parser")



    prices = [float(i.replace('\n', ' ').strip().replace(' ', '.')) for i in prices]
    sales = [re.search('\d+', str(sale)).group() for sale in sales]

    prices_kosm = [float(str(i).replace('\n', ' ').strip().replace(' ', '.')) for i in prices_kosm]
    sales_kosm = [re.search('\d+', str(sale)).group() for sale in sales_kosm]
    magnit_df = pd.DataFrame({'Наименование': names,
                              'Ссылка': links,
                              'Цена': prices,
                              'Скидка': sales})
    magnit_kosm_df = pd.DataFrame({'Наименование': names_kosm,
                                   'Ссылка': links_kosm,
                                   'Цена': prices_kosm,
                                   'Скидка': sales_kosm})

    magnit_df = magnit_df[~magnit_df['Наименование'].isin(magnit_kosm_df['Наименование'])].reset_index(
        drop=True)  # удалаяю из магнита, то что есть в косметик

    magnit_df = magnit_df.sort_values(by='Скидка', ascending=False)
    magnit_kosm_df = magnit_kosm_df.sort_values(by='Скидка', ascending=False)
    return {'Магнит': magnit_df, 'Магнит_Косметик': magnit_kosm_df}


if __name__ == '__main__':

    for name, pd in magnit().items():
        pd.to_excel(f'{name}.xlsx',index=False)
