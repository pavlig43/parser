import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def availability(page, lst, tag_name):  # Добавляет 0 в значение, если оно отсутствует у карточки товара(цена,скидка и т.д)
    try:
        lst.append(page.find(tag_name[0], tag_name[1]).text)
    except:
        lst.append(0)
def get_bs4(url):
    ua = UserAgent().random
    headers = {'User-Agent': ua}

    page_get = requests.get(url, headers=headers, cookies={'mg_geo_id': '1795'}, timeout=5)

    page = BeautifulSoup(page_get.text, 'html.parser')
    return page

#if __name__ == '__main__':


