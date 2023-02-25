import re

import pandas as pd
from bs4 import BeautifulSoup

from catalog import catalog
from sort_df import sort_df


def agrok():
    names = []
    links = []
    prices_sales = []
    for i in range(1, 12):
        # url = f'https://agrokomplexshop.ru/landings/all_skidki/?PAGEN_2={i}&ajax_get=Y&AJAX_REQUEST=Y&bitrix_include_areas=N'
        # page_get = requests.get(url)
        # page = BeautifulSoup(page_get.text, 'html.parser')
        html_page = open(f'Html_lst/page{i}.html', 'r')
        page = BeautifulSoup(html_page, 'html.parser')
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
    agrokomplex_df = pd.DataFrame({'Наименование': names,
                                   'Ссылка': links,
                                   'Цена': [i[0] for i in prices_sales],
                                   'Скидка': [i[1] for i in prices_sales]})
    sort_df(agrokomplex_df, catalog)
if __name__ == '__main__':
    agrok()




