def sort_df(name_df, catalog):
    name_df = name_df[name_df.Ссылка.str.contains('|'.join(catalog))] #отбор товаров из каталога
    name_df = name_df.sort_values(by='Скидка', ascending=False)
    name_df = name_df.drop_duplicates(keep='first')
    name_df.to_excel('Список.xlsx')