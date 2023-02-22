import os
import requests


def save_website(name_of_directory, url,
                 name_of_page='page1', ):  # ''' Передаем url и сохраняем эти страницы с нужным именем в
    #	папке Html_lst, имя лучше использовать f'page{номер страницы}' при прохождении цикла '''
    if 'Html_lst' not in os.listdir(name_of_directory):
        os.makedirs(f'{name_of_directory}/Html_lst')
    r = requests.get(url)
    html = r.text
    file = open(f'agrokomplex/Html_lst/{name_of_page}.html', 'w')
    file.write(html)
    file.close()




