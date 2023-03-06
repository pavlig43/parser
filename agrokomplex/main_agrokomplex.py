import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from fake_useragent import UserAgent

from catalog import catalog



def agrok():
    names = []
    links = []
    prices_sales = []
    for i in range(1, 12):
        url = f'https://agrokomplexshop.ru/landings/all_skidki/?PAGEN_2={i}&ajax_get=Y&AJAX_REQUEST=Y&bitrix_include_areas=N'
        headers = {'User-Agent': UserAgent().chrome}
        page_get = requests.get(url,headers=headers)
        page = BeautifulSoup(page_get.text, 'html.parser')
        prices_sales_block = page.find_all('div', {'class': 'price_matrix_wrapper'})
        for i in prices_sales_block:  # блок с ценами и скидками
            price = i.find('div', {'class': 'price font-bold font_mxs'}).text.replace('\n', '')
            try:
                sale = i.find('div', {'class': 'value'}, 'span').text
                sale = int(re.search('\d+', sale).group())
            except AttributeError:
                sale = 0

            prices_sales.append((price, sale))

        links += page.find_all('a', {'class': "dark_link js-notice-block__title option-font-bold font_sm"})
        names += page.find_all('div', {'class': 'item-title'})

    names = [name.text for name in names]
    links = [f"https://agrokomplexshop.ru{link.get('href')}" for link in links]
    agrokomplex_df: DataFrame = pd.DataFrame({'Наименование': names,
                                   'Ссылка': links,
                                   'Цена': [i[0] for i in prices_sales],
                                   'Скидка': [i[1] for i in prices_sales]})


    agrokomplex_df = agrokomplex_df[agrokomplex_df.Ссылка.str.contains('|'.join(catalog))]#отбор из каталога нужных категорий
    agrokomplex_df = agrokomplex_df.sort_values(by='Скидка', ascending=False)
    agrokomplex_df = agrokomplex_df.drop_duplicates(keep='first')
    agrokomplex_df.to_excel('1.xlsx')
if __name__ == '__main__':
    agrok()




