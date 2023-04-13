from tkinter import *

def a():

    root1 = Tk()
    root1.geometry("500x500")
    root1.title('Выбери город')
    cities = ['г.Новочебоксарск', 'г.Саратов', 'г.Соль-Илецк', 'г.Хотьково', 'г.Осинники', 'г.Новокузнецк', 'г.Омск']

    def filter_cities(*args):
        # Получаем текст, введенный пользователем
        text = city_entry.get()
        # Фильтруем список городов, оставляем только те, которые содержат это слово
        filtered_cities = [city for city in cities if text.lower() in city.lower()]
        # Обновляем список городов в Listbox
        city_listbox.delete(0, END)
        for city in filtered_cities:
            city_listbox.insert(END, city)

    # Создаем виджеты Entry и Listbox
    city_entry = Entry(root1,background='#999999' )
    city_listbox = Listbox(root1)

    # Связываем ввод пользователя с обработчиком filter_cities
    city_entry.bind("<KeyRelease>", filter_cities)

    # Размещаем виджеты на окне
    city_entry.pack()
    city_listbox.pack()

    root1.mainloop()




if __name__ == '__main__':
    a()