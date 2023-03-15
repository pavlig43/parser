from bs4 import BeautifulSoup

def get_all_category():
    html = open('change.html', 'r', encoding='utf-8')
    page_text = BeautifulSoup(html, 'html.parser')
    category_dict = {}

    category_name = page_text.find_all('li', class_='categories-item')
    for category in category_name:
        name_of_category = category.find('h4').text.strip()
        # ищу имена сабкатегорийй в основных
        subcutegories_names = [i.text.strip() for i in category.find_all('label', class_='radio-wrap')]
        # ищу номер категорий в этих именах сабкатегорий
        subcutegories_values = [i.find('input').get('value') for i in category.find_all('label', class_='radio-wrap')]
        category_dict[name_of_category] = {value: sub for sub, value in zip(subcutegories_names, subcutegories_values)}
    return category_dict

if __name__ == '__main__':
    print(get_all_category())
    # nd = {}
    # for i in category_dict.values():
    #     nd |=i
    # print(nd)

