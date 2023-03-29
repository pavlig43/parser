import json
import os

from ttkwidgets import CheckboxTreeview as Tree


class CheckboxTreeview(Tree):

    def item_check(self, item):
        """Check item and propagate the state change to ancestors and descendants."""
        self._check_ancestor(item)
        self._check_descendant(item)

    def item_uncheck(self, item):
        """Uncheck item and propagate the state change to ancestors and descendants."""
        self._uncheck_descendant(item)
        self._uncheck_ancestor(item)
    
class MyJson:
    filepath = ''
    def __init__(self, bolder_shop, name):
        self.name = name
        self.bolder_shop = bolder_shop
        MyJson.filepath = rf'C:\Users\user\PycharmProjects\parser\shops\{self.bolder_shop}\{self.name}.json'
    def read_my_choice(self):
        if not os.path.exists(MyJson.filepath):
            open(MyJson.filepath,'w').close()# создаю файл, если нет
        try:
            with open(MyJson.filepath, 'r') as file:
                my_choice = file.read()
                return json.loads(my_choice)
        except json.decoder.JSONDecodeError:
            return {}

    def write_my_choice(self,dict_my_new_choice):# передаю словарь , полученный из тк в json файл
        my_choice_str = json.dumps(dict_my_new_choice, ensure_ascii=False)  # с русским текстом
        with open(MyJson.filepath, 'w') as file:
            file.write(my_choice_str)
