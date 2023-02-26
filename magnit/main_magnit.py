import re

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
    names_kosm = []
    links_kosm = []
    prices_kosm = []
    sales_kosm = []
    # url = https://magnit.ru/promo/
    # page_get = requests.get(url,cookies={'mg_geo_id': '1795'})
    # page = BeautifulSoup(page_get.text, 'html.parser')
    html_page = open(f'Html_lst/page{1}.html', 'r')
    page = BeautifulSoup(html_page, 'html.parser')
    all_products = page.find_all('a', {'class': 'card-sale card-sale_catalogue'})
    for good in all_products:
        if good.find('div', {'class': 'label label_sm label_magnit card-sale__discount'}):
            availability(good, sales, tag_name=('div', {'class': 'label label_sm label_magnit card-sale__discount'}))
            availability(good, names, tag_name=('div', {'class': 'card-sale__title'}))
            links.append(f'https://magnit.ru{good.get("href")}')
            availability(good, prices, tag_name=('div', {'class': 'label__price label__price_new'}))
        else:
            availability(good, sales_kosm, tag_name=('div', {'class': 'label label_sm label_cosmetic card-sale__discount'}))
            availability(good, names_kosm, tag_name=('div', {'class': 'card-sale__title'}))
            links_kosm.append(f'https://magnit.ru{good.get("href")}')
            availability(good, prices_kosm, tag_name=('div', {'class': 'label__price label__price_new'}))

    prices = [float(i.replace('\n', ' ').strip().replace(' ', '.')) for i in prices]
    sales = [re.search('\d+', str(sale)).group() for sale in sales]

    prices_kosm = [float(i.replace('\n', ' ').strip().replace(' ', '.')) for i in prices_kosm]
    sales_kosm = [re.search('\d+', str(sale)).group() for sale in sales_kosm]
    magnit_df = pd.DataFrame({'Наименование': names,
                              'Ссылка': links,
                              'Цена': prices,
                              'Скидка': sales})
    magnit_kosm_df = pd.DataFrame({'Наименование': names_kosm,
                              'Ссылка': links_kosm,
                              'Цена': prices_kosm,
                              'Скидка': sales_kosm})
    sort_df(magnit_df)
    sort_df(magnit_kosm_df)
    #magnit_df = magnit_df(magnit_df['Наименование'] != magnit_kosm_df['Наименование'])
    magnit_df = magnit_df[~magnit_df['Наименование'].isin(magnit_kosm_df['Наименование'])].reset_index(drop=True)

    magnit_df.to_excel('magnit.xlsx', index=False)
    magnit_kosm_df.to_excel('names_kosm.xlsx', index=False)


if __name__ == '__main__':
    magnit()
