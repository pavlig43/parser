import re
from collections import defaultdict

import pandas as pd
from bs4 import BeautifulSoup

# from catalog import catalog
from sort_df import sort_df
from availability import availability


def magnit():
    names = []
    links = []
    prices = []
    sales = []
    # url = f'https://agrokomplexshop.ru/landings/all_skidki/?PAGEN_2={i}&ajax_get=Y&AJAX_REQUEST=Y&bitrix_include_areas=N'
    # page_get = requests.get(url)
    # page = BeautifulSoup(page_get.text, 'html.parser')
    html_page = open(f'Html_lst/page{1}.html', 'r')
    page = BeautifulSoup(html_page, 'html.parser')
    all_products = page.find_all('a', {'class': 'card-sale card-sale_catalogue'})
    for good in all_products:
        availability(good, names, tag_name=('div', {'class': 'card-sale__title'}))
        links.append(f'https://magnit.ru{good.get("href")}')
        availability(good, prices, tag_name=('div', {'class': 'label__price label__price_new'}))
        availability(good, sales, tag_name=('div', {'class': ['label label_sm label_magnit card-sale__discount',
                                                              'label label_sm label_cosmetic card-sale__discount']}))
    prices = [float(i.replace('\n', ' ').strip().replace(' ', '.')) for i in prices]
    sales = [re.search('\d+', str(sale)).group() for sale in sales]
    magnit_df = pd.DataFrame({'Наименование': names,
                              'Ссылка': links,
                              'Цена': prices,
                              'Скидка': sales})
    sort_df(magnit_df)


if __name__ == '__main__':
    magnit()
