import os
import requests


def save_website(name_of_directory, url,
                 name_of_page='page1', cookies=''):  # ''' Передаем url и сохраняем эти страницы с нужным именем в
    #	папке Html_lst, имя лучше использовать f'page{номер страницы}' при прохождении цикла '''
    if 'Html_lst' not in os.listdir(name_of_directory):
        os.makedirs(f'{name_of_directory}/Html_lst')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    if cookies:
        r = requests.get(url, headers=headers, cookies=cookies)
    else:
        r = requests.get(url, headers=headers,)
    r.encoding = 'utf-8'
    html = r.text
    file = open(f'{name_of_directory}/Html_lst/{name_of_page}.html', 'w')
    file.write(html)
    file.close()
