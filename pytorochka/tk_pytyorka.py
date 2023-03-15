import tkinter as tk
import json


def tk_category():
    old_men = {'олег': '35', 'паша': '30', 'вася': '25', 'коля': '20', 'жора': '15', 'макс': '10'}
    # men = {'олег':'35','паша':'30','вася':'25','коля':'20'}
    # men_json_str = json.dumps(men, ensure_ascii=False) # с русским текстом
    # with open('men.json','w') as file:
    # 	file.write(men_json_str)
    with open('men.json', 'r') as file:
        men_str = file.read()
    men = json.loads(men_str)

    def saved():
        new_dict = {}
        for key, value in old_men.items():
            if var_dict[key].get() == True:
                new_dict[key] = value
        print(new_dict)
        men_json_str = json.dumps(new_dict, ensure_ascii=False)  # с русским текстом
        with open('men.json', 'w') as file:
            file.write(men_json_str)
        root.destroy()

    root = tk.Tk()
    var_dict = {}
    for i, (key, value) in enumerate(old_men.items()):
        if key in men:
            var_dict[key] = tk.BooleanVar(value=True)
        else:
            var_dict[key] = tk.BooleanVar()
        tk.Checkbutton(root, text=key, variable=var_dict[key]).grid(row=i, column=0)
    tk.Button(root, text='SAVE', command=saved).grid(row=len(old_men))
    root.mainloop()


if __name__ == '__main__':
    tk_category()
