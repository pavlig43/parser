import re

from bs4 import BeautifulSoup


def choice_category(page):
    lst_category = page.find_all(class_='checkbox')
    dict_category = {
        '0': ('мой выбор', 'https://magnit.ru/promo/?category[]=fruits_vegetables&category[]=moloko&category[]=myaso')}
    for number, i in enumerate(lst_category):
        try:
            name = i.text.replace('\n', '')
            bit_url = i.find(class_="checkbox__control", id=re.compile('cat_')).get('value').strip()
            bit_url = f'https://magnit.ru/promo/?category[]={bit_url}'
            dict_category[str(number + 1)] = (name, bit_url)
        except AttributeError:
            continue
    for i, j in  dict_category.items():
        print(f'{i}------{j[0]}')
    url = dict_category[input('какой номер?')][1]
    return url


# if __name__ == '__main__':



