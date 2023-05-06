import json
import time
from bs4 import BeautifulSoup

from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


def cities_magnit():
    url = 'https://magnit.ru/shops/'
    ua = UserAgent().random

    options = Options()

    options.add_experimental_option('detach', True)
    options.add_argument(f'user-agent={ua}')

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # нажимаю на кнопку выбора города
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[1]/a/span[2]')))
    btn.click()
    driver.maximize_window()
    time.sleep(1)

    # дплее 3 строки получают список регионов России
    html_regions = [i.find_element(By.TAG_NAME, 'a') for i in driver.find_elements(By.CLASS_NAME, 'city-search__item')]
    list_regions = [i.get_attribute('textContent') for i in html_regions if
                    i.get_attribute('class') == 'city-search__link js-region']




    # page = driver.page_source
    # page = BeautifulSoup(page, 'html.parser')
    # all_cities = []
    # for i in list_regions:
    #     entry_input = driver.find_element(By.NAME, "citySearch")
    #     entry_input.clear()
    #     entry_input.send_keys(i)
    #     time.sleep(2)
    #     page = driver.page_source
    #     page = BeautifulSoup(page, 'html.parser')
    #     cities = page.find_all('div', {'class': "city-search__item ui-menu-item"})
    #     cities = [i.get('data-value') for i in cities]
    #     all_cities += cities
    # mg_geo_id = {}
    # with open('city.txt', 'w') as f:
    #     f.write('%'.join(all_cities))

    #mg_geo_id = {}
    with open('errors.txt', 'r') as f:
        all_cities = f.read().split('%')
    with open('cookie_magnit.json', 'r',encoding='utf-8')  as f:
        mg_geo_id = f.read()
        mg_geo_id = json.loads(mg_geo_id)

    def get_cookie(city):
        entry_input = driver.find_element(By.NAME, "citySearch")

        entry_input.clear()
        entry_input.send_keys(city)

        btn_city = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[5]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/ul/div[1]/a')))
        btn_city.click()

        time.sleep(2)
        try:
            btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[1]/a/span[2]')))
            btn.click()
        except:
            btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[1]/a/span[2]')))
            btn.click()

        cookie = driver.get_cookie('mg_geo_id')

        try:
            id_city = cookie['value']

            kind_shops = BeautifulSoup(driver.page_source,'html.parser')
            kind_shops = kind_shops.find_all('span',{'class':'g-button__text'})
            kind_shops = [i.text for i in kind_shops]
            mg_geo_id[city] = (id_city,kind_shops)
        except:
            mg_geo_id[city] = 'N/D'

        time.sleep(2)
    errors_city=[]
    for city in all_cities:
        try:
            get_cookie(city)
        except:
            errors_city.append(city)
    try:
        with open('errors.txt', 'w') as f:
            f.write('%'.join(errors_city))
    except:
        pass
    print(mg_geo_id)
    with open('cookie_magnit.json', 'w',encoding='utf-8') as cookie:
        mg_geo_id = json.dumps(mg_geo_id,ensure_ascii=False)
        cookie.write(mg_geo_id)





    # btn_choce_city = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/ul/div/a')))# ажимаю на город ввыпадающем спичке

    # btn_choce_city.click()

    # print(*[i.get_attribute('outerHTML') for i in list_shops])
    # print([ for i in list_shops])


if __name__ == '__main__':
    cities_magnit()
