import pandas as pd

from category import get_all_category


def get_one_dict_subcutegories(my_dict):
    name_new_dict = {}
    for i in my_dict.values():
        name_new_dict |= i
    return name_new_dict


class Choice(dict):

    def show_all_category(self):
        for name, value in self.items():
            print(f'{name}:{value}')
    def my_choice(self):
        self.show_all_category()
        my_lst = []
        my_lst += input('Выбери').split(',')
        return my_lst


if __name__ == '__main__':
    a = Choice(get_one_dict_subcutegories(get_all_category()))
    s = pd.Series(a)
    s.to_excel('1.xlsx')


