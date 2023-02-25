import requests
import os

from save_website import save_website

if __name__ == '__main__':
    save_website('magnit', 'https://magnit.ru/promo/', cookies={'mg_geo_id': '1795'})
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    # url = 'https://magnit.ru/promo/'
    # r = requests.get(url, headers=headers)
    # print(r.text)
