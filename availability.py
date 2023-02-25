def availability(page, lst, tag_name):  # Добавляет 0 в значение, если оно отсутствует у карточки товара(цена,скидка и т.д)
    try:
        lst.append(page.find(tag_name[0], tag_name[1]).text)
    except:
        lst.append(0)

