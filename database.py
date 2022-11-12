
import os
import random
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import datetime
# from prettytable import PrettyTable # Модуль PrettyTable в Python, вывод табличных данных (python -m pip install -U prettytable)

connect = sqlite3.connect('dbBot/ExchangeRates.db',  # Создаём/подключаем Базу данных
                          check_same_thread=False)  # Обеспечиваем единый поток
cursor = connect.cursor()  # Создаем объект cursor (курсор), который позволяет нам взаимодействовать с базой данных


# функция проверки наличия таблицы в базе данных
def fun_checking_if_table_exists(name_tabl):
    # get the count of tables with the name (получить количество таблиц с именем)
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? ''',(name_tabl,))
    return cursor.fetchone()[0]  # возвращаем количество 0 или 1,2,3 :)


# функция создания таблицы пользователя
def fun_table_users():
    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS(
         idChat INTEGER not NULL PRIMARY KEY,
         first_name TEXT,
         last_name TEXT,
         username TEXT,
         type TEXT,
         city_user TEXT,
         url_user Text);
         ''')
    cursor.connection.commit()  # сохраним изменения


# Функция регистрации пользователя
def fun_reg_user(idChat, first_name, last_name, username, type,
                 city_user = 'Молодечно', url_user = 'https://myfin.by/currency/molodechno'):

    cursor.execute(''' SELECT idChat FROM USERS WHERE idChat= ?''', (idChat,))
    count = cursor.fetchall()

    # if self.cursor.fetchone() == []:  # если такого пользователя нет
    if count == []:  # если такого пользователя нет
        cursor.execute(''' INSERT INTO USERS (idChat, first_name, last_name, username, type, city_user, url_user) 
                                VALUES (?,?,?,?,?,?,?) ; ''',
                       (idChat, first_name, last_name, username, type, city_user, url_user))
        cursor.connection.commit()  # сохраним изменения
        cursor.execute(f''' SELECT * FROM USERS WHERE idChat=? ''', (idChat,))
        print('Зарегистрирован новый пользователь: ', cursor.fetchall())
    else:
        print('Пльзователь уже зарегистрирован:')
        cursor.execute(''' SELECT * FROM USERS WHERE idChat=? ''', (idChat,))
        print(cursor.fetchall())


# функция регистрации изменения в таблице USERS - города пользователя. Принимает новый город и...
def fun_set_user_city_update(idChat, city):
    cursor.execute('''  UPDATE USERS SET city_user=?  WHERE idChat=? ''', (city, idChat))
    cursor.connection.commit()  # сохраним изменения
    cursor.execute('''  UPDATE USERS SET url_user = (SELECT wwwCity
                        FROM USERS
                        LEFT JOIN BANK_CITY
                        WHERE USERS.city_user = BANK_CITY.city GROUP BY wwwCity)
                        WHERE  idChat=?
                        ''', (idChat,))
    cursor.connection.commit()  # сохраним изменения


# функция создания и заполнения банков городов
def fun_table_bank_city():
    global city
    cursor.execute('''CREATE TABLE IF NOT EXISTS BANK_CITY(
                    idBankCity INTEGER PRIMARY KEY AUTOINCREMENT,
                    wwwCity TEXT,
                    city TEXT,
                    bank TEXT,
                    address  TEXT,
                    mode  TEXT);
                    ''')

    list_line = []
    with open('dbBot/bank_city.txt',
              'r') as f:  # справочный файл размещен в папке 'dbBot', директории где находится исполняемый файл Python
        for line in f.readlines():
            line = line.split('\t')  # разделим нашу строку на строки по сиволу табуляции
            line = [s.strip() for s in line]  # удалим сивол переноса строки
            # стоит заметить, что .strip() также удаляет любой пробел в начале и в конце строки
            tuple_line = tuple(line)
            if tuple_line[0] == '':
                continue  # пропустим кортеж с пустыми значениями (символ переноса строки, который ранее был удален .strip(), но пустой элемент кортежа остался
            list_line.append(tuple_line)
        # print(list_line)
        for i in range(len(list_line)):
            cursor.execute(
                    '''INSERT INTO BANK_CITY (wwwCity, city, bank, address, mode) VALUES(?,?,?,?,?)''',
                    (list_line[i][0], list_line[i][1], list_line[i][2],
                     list_line[i][3], list_line[i][4]))

        cursor.connection.commit()  # сохраним изменения
        f.close()


# функция создания таблицы  городов-банков для ID.пользователя
def fun_table_bank_city_users():
    cursor.execute('''CREATE TABLE IF NOT EXISTS BANK_CITY_USERS(
                 idBankCityUsers INTEGER PRIMARY KEY AUTOINCREMENT,
                     elected INTEGER DEFAULT 1,
                     bankCity TEXT,
                     idChat INTEGER NOT NULL,
                     FOREIGN KEY (idChat) REFERENCES USERS (idChat)
                     ON DELETE CASCADE ON UPDATE NO ACTION  );''')
    cursor.connection.commit()  # сохраним изменения


# функция заполнения таблицы  BANK_CITY_USERS - банков города ID.пользователя
def fun_set_bank_city_users(idChat):
    # не будем заморачиваться с обновлением данных по пользователю в этой таблице
    # просто удалим если они были
    cursor.execute(f'''  DELETE FROM BANK_CITY_USERS WHERE idChat = ?''', (idChat,))
    cursor.connection.commit()  # сохраним изменения
    # заполним таблицу для пользователя
    cursor.execute('''  INSERT INTO BANK_CITY_USERS (bankCity, idChat)
                        SELECT BANK_CITY.bank, USERS.idChat
                        FROM USERS
                        LEFT JOIN BANK_CITY 
                        WHERE USERS.city_user = BANK_CITY.city AND idChat = ?  
                        GROUP BY bank
                        ''',(idChat,))
    cursor.connection.commit()  # сохраним изменения


# функция возвращает список строк доступных городов в БД
def fun_get_cities():
    cursor.execute('''SELECT city  FROM BANK_CITY  GROUP BY city; ''')
    cityDB = [str(item) for sub in cursor.fetchall() for item in sub]
    return cityDB # ['Вилейка', 'Заславль', 'Молодечно', 'Мядель', 'Нарочь', 'Радошковичи']


# функция создания таблицы курсов
def fun_table_exchange_rates():
    cursor.execute('''CREATE TABLE IF NOT EXISTS EXCHANGE_RATES(
                 idExchangeRates INTEGER PRIMARY KEY AUTOINCREMENT,
                 date_time TEXT,
                 city_bank TEXT,
                 bank_exchange TEXT,
                 USD_buys REAL,
                 USD_sells REAL,
                 EUR_buys REAL,
                 EUR_sells REAL,
                 RUB100_buys REAL,
                 RUB100_sells REAL,
                 EUR_USD_buys REAL,
                 EUR_USD_sells REAL);
                 ''')
    cursor.connection.commit()  # сохраним изменения


# функция загрузки/обновления таблицы курсов
def fun_set_courses(idChat):
    # заголовки - описывают пользователя - (в гугле сделать запрос "my user agent")
    # (если их не передать то будет считаться что заходит бот и запрос не будет обработан)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', }

    # названия банков загрузим из таблицы 'BANK_CITY_USERS', отбор по id пользователя
    cursor.execute('''SELECT bankCity FROM BANK_CITY_USERS WHERE idChat=? ''', (idChat,))
    list_selected = cursor.fetchall()
    # [('Банк БелВЭБ',), ('Белагропромбанк',), ('Беларусбанк',), ('Белгазпромбанк',), ('Белинвестбанк',), ('МТБанк',), ('Приорбанк',), ('Сбер Банк',)]
    list_selected_banks = []  # избранный список банков пользователем
    for s in list_selected:   # преобразуем список кортежей банков в список строк
        list_selected_banks.append(''.join(s))
        # ['Банк БелВЭБ', 'Белагропромбанк', 'Беларусбанк', 'Белгазпромбанк', 'Белинвестбанк', 'МТБанк', 'Приорбанк', 'Сбер Банк']

    # получим url для пользователя
    cursor.execute('''SELECT city_user, url_user
                    FROM USERS
                    WHERE  idChat = ? ''',(idChat,))

    city = cursor.fetchone() # сохраним в переменную город пользователя кирилицей  url для парсинга
    # city[0] - Молодечно
    # city[1] - # https://myfin.by/currency/molodechno

    # Для начала проверим есть ли в таблице курсов данные по требуемому населенному пункту
    cursor.execute('''SELECT COUNT(city_bank)
                    FROM EXCHANGE_RATES
                    LEFT JOIN USERS
                    WHERE city_bank = city_user AND idChat=? ''', (idChat,))
    count_city_bank = cursor.fetchone()

    if int(count_city_bank[0]): # если для данного города уже есть загруженные курсы
        # ограничем при необходимости количесто парсинга по требуемому городу - не чаще 1/10мин
        cursor.execute('''SELECT strftime('%s','now', 'localtime') - strftime('%s',date_time)
                          FROM EXCHANGE_RATES
                          LEFT JOIN USERS
                          WHERE city_bank = city_user AND idChat=? ''', (idChat,))
        city_datetime = cursor.fetchone()
        if int(city_datetime[0]) <= 600:
            print(f'С момента обновления курсов для {city[0]}, прошло {city_datetime[0]} секунд')
            return
        else: # данные есть, но пришло время обновляться
            # парсим сайт
            res = requests.get(city[1], headers).text  # отправим запрос на сайт
            soup = BeautifulSoup(res, 'lxml')  # получим всю страницу

            for tables in soup.select("table tr"):  # выберем все значения из ячеек таблиц страницы
                bank_rate = [item.get_text(strip=True) for item in tables.select("td")]
                if bank_rate == []:
                    continue
                if bank_rate[0] in list_selected_banks:  # нас интересуют все строки таблиц в первой ячейке которых указан один из наших выбранных банков
                    cursor.execute('''UPDATE EXCHANGE_RATES SET date_time=datetime('now','localtime'), city_bank=?,
                    bank_exchange=?, USD_buys=?, USD_sells=?, EUR_buys=?, EUR_sells=?,
                    RUB100_buys=?, RUB100_sells=?, EUR_USD_buys=?, EUR_USD_sells=?
                    WHERE city_bank=? AND bank_exchange=? ''',
                    (city[0],bank_rate[0],bank_rate[1],bank_rate[2],bank_rate[3],bank_rate[4],
                    bank_rate[5],bank_rate[6],bank_rate[7],bank_rate[8],city[0],bank_rate[0]))
    else:# если мы здесь, то данных о курсах банков в требуемом городе нет
        # парсим сайт
        res = requests.get(city[1], headers).text  # отправим запрос на сайт
        soup = BeautifulSoup(res, 'lxml')  # получим всю страницу
        for tables in soup.select("table tr"):  # выберем все значения из ячеек таблиц страницы
            bank_rate = [item.get_text(strip=True) for item in tables.select("td")]
            if bank_rate == []:
                continue
            if bank_rate[0] in list_selected_banks:  # нас интересуют все строки таблиц в первой ячейке которых указан один из наших выбранных банков
                # cursor.execute('''SELECT * FROM EXCHANGE_RATES  WHERE city_bank = ? AND bank_exchange = ? ''', (city[0],bank_rate[0]))
                cursor.execute('''INSERT INTO EXCHANGE_RATES (date_time, city_bank, bank_exchange, USD_buys, USD_sells,
                            EUR_buys, EUR_sells, RUB100_buys, RUB100_sells, EUR_USD_buys, EUR_USD_sells)
                            VALUES(datetime('now', 'localtime'),?,?,?,?,?,?,?,?,?,?)''',
                                (city[0], bank_rate[0], bank_rate[1], bank_rate[2], bank_rate[3], bank_rate[4],
                                 bank_rate[5], bank_rate[6], bank_rate[7], bank_rate[8]))
    cursor.connection.commit()  # сохраним изменения


# функция возращает список кортежей загруженных курсов
def fun_all_courses(city_bank = 'Молодечно'):
    cursor.execute('''SELECT bank_exchange, USD_buys, USD_sells, EUR_buys, EUR_sells,
                                    RUB100_buys, RUB100_sells, EUR_USD_buys, EUR_USD_sells, date_time
                                    FROM EXCHANGE_RATES  WHERE city_bank = ?''',(city_bank,))
    cursor.connection.commit()  # сохраним изменения
    return cursor.fetchall()


# функция возращает форматированную строку с курсами всех банков для передачи в message
def fun_form_all_courses(idChat):
    cursor.execute('''SELECT city_user
                    FROM USERS
                    WHERE  idChat = ? ''',(idChat,))
    city = cursor.fetchone() # сохраним в переменную город пользователя кирилицей  url для парсинга
    list_cur = fun_all_courses(city[0]) # список кортежей загруженных курсов
    Scourses = (list_cur[0][9])[:16] + '         ' +  city[0].upper()  + '\nБанк' + 'покупает / продает \n'.rjust(41, ' ')

    for element in list_cur:
        Scourses += ('=' * 31) + '\n '
        Scourses += (''.join(map(str, element[0])))+ '\n'
        Scourses += 'USD   '.rjust(29, ' ') + ('{:7.4f}  /  {:7.4f}'.format(element[1], element[2])) + '\n'
        Scourses += 'EUR   '.rjust(29, ' ') + ('{:7.4f}  /  {:7.4f}'.format(element[3], element[4])) + '\n'
        Scourses += '100 RUB   '.rjust(25, ' ') + ('{:7.4f}  /  {:7.4f}'.format(element[5], element[6])) + '\n'
        Scourses += 'EUR / USD   '.rjust(24, ' ') + ('{:7.4f}  /  {:7.4f}'.format(element[7], element[8])) + '\n'
    Scourses += ('=' * 31)
    return Scourses


# функция возращает лучшие курсы
def fun_best_courses(idChat):
    # для работы функции необходим иходный город зарегестрированный для пользователя,
    city_bank = fun_get_city_user(idChat)  # получим и определяем требуемый город
    list_cur = fun_all_courses(city_bank)    # получим список кортежей с курсами банков
    list_best_cur = []  # сюда соберем лучшие курсы (покупка - max; продажа - min)
    # [USD Покупает/Продает - 0,1 элемент, EUR Покупает/Продает - 2,3 элемент, 100RUB Покупает/Продает - 4,5 элемент, EUR/USD Покупает/Продает - 6,7 элемент, ]
    # [[Банк, Покупает], [Банк, Продает], [Банк, Покупает], [Банк, Продает],[Банк, Покупает], [Банк, Продает],[Банк, Покупает], [Банк, Продает]]
    for element in list_cur:  # цикл по кортежам - элементам списка
        if not len(list_best_cur):
            list_best_cur = [[element[0], element[1]], [element[0], element[2]],  # USD
                             [element[0], element[3]], [element[0], element[4]],  # EUR
                             [element[0], element[5]], [element[0], element[6]],  # 100RUB
                             [element[0], element[7]], [element[0], element[8]]]  # EUR / USD
            continue

        if element[1] > list_best_cur[0][1]:
            list_best_cur[0][0] = element[0]
            list_best_cur[0][1] = element[1]

        if element[2] < list_best_cur[1][1]:
            list_best_cur[1][0] = element[0]
            list_best_cur[1][1] = element[2]

        if element[3] > list_best_cur[2][1]:
            list_best_cur[2][0] = element[0]
            list_best_cur[2][1] = element[3]

        if element[4] < list_best_cur[3][1]:
            list_best_cur[3][0] = element[0]
            list_best_cur[3][1] = element[4]

        if element[5] > list_best_cur[4][1]:
            list_best_cur[4][0] = element[0]
            list_best_cur[4][1] = element[5]

        if element[6] < list_best_cur[5][1]:
            list_best_cur[5][0] = element[0]
            list_best_cur[5][1] = element[6]

        if element[7] > list_best_cur[6][1]:
            list_best_cur[6][0] = element[0]
            list_best_cur[6][1] = element[7]

        if element[8] < list_best_cur[7][1]:
            list_best_cur[7][0] = element[0]
            list_best_cur[7][1] = element[8]

    return list_best_cur


# # функция возращает дату, время загруженных курсов
# def fun_datetime_courses(city = 'Молодечно'):
#     cursor.execute(
#         '''SELECT date_time FROM EXCHANGE_RATES  WHERE citi_bank = ? GROUP BY date_time ''',(city,))
#     cursor.connection.commit()  # сохраним изменения
#     return cursor.fetchone()


# функция возращает город пользователя (ru)
def fun_get_city_user(idChat):
    cursor.execute('''SELECT city_user FROM USERS  WHERE idChat=? ''', (idChat,))
    city_user = cursor.fetchone()
    return city_user[0]


# функция выбора случайных картинок
def fun_image_file_name(dir='images'):
    list_img = []
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if root == '.\\' + dir:
                new_file = root[2:] + '/' + filename
                list_img.append(new_file)
    # img = ' '.join(map(str, (random.choices(list_img, weights=None, cum_weights=None, k=1))))  # случайный файл
    img = ' '.join(map(str, (random.choices(list_img))))  # случайный файл
    return img  # images/89334773_r3Pw_yMtdjw.jpg


# функция возвращает форматировааную строку банков с личшеми курсами покупки/продажи
# Проработан вариант информирования о лучших курсах с данными других банков
def get_top_buys(idChat, currency): # аргументы id чата(пользователя) и требуемая валюта и направление сделки ('buys' или 'sells')
    top_list_source_tuples = []
    other_list_source_tuples = []

    if currency.find('buys') != -1: # задача - подогнать запрос под любую валюту, в названии столбца которого есть   'buys'
        cursor.execute(f'''SELECT date_time, city_bank, bank_exchange, {currency}
                          FROM EXCHANGE_RATES
                          LEFT JOIN USERS
                          WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                          AND USERS.idChat = ?
                          AND {currency} = (SELECT MAX({currency})
                          FROM EXCHANGE_RATES
                          LEFT JOIN USERS
                          WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                          AND USERS.idChat = ?)
						  ORDER BY {currency} DESC''', (idChat,idChat,))
        top_list_source_tuples = cursor.fetchall()

        cursor.execute(f'''SELECT date_time, city_bank, bank_exchange, {currency}
                                  FROM EXCHANGE_RATES
                                  LEFT JOIN USERS
                                  WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                                  AND USERS.idChat = ?
                                  AND {currency} != (SELECT MAX({currency})
                                  FROM EXCHANGE_RATES
                                  LEFT JOIN USERS
                                  WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                                  AND USERS.idChat = ?)
        						  ORDER BY {currency} DESC''', (idChat, idChat,))
        other_list_source_tuples = cursor.fetchall()

    elif currency.find('sells') != -1: # задача - подогнать запрос под любую валюту, в названии столбца которого есть   'sells'
        cursor.execute(f'''SELECT date_time, city_bank, bank_exchange, {currency}
                          FROM EXCHANGE_RATES
                          LEFT JOIN USERS
                          WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                          AND USERS.idChat = ?
                          AND {currency} = (SELECT MIN({currency})
                          FROM EXCHANGE_RATES
                          LEFT JOIN USERS
                          WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                          AND USERS.idChat = ?)
                          GROUP BY {currency}, bank_exchange''', (idChat,idChat,))
        top_list_source_tuples = cursor.fetchall()

        cursor.execute(f'''SELECT date_time, city_bank, bank_exchange, {currency}
                                  FROM EXCHANGE_RATES
                                  LEFT JOIN USERS
                                  WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                                  AND USERS.idChat = ?
                                  AND {currency} != (SELECT MIN({currency})
                                  FROM EXCHANGE_RATES
                                  LEFT JOIN USERS
                                  WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                                  AND USERS.idChat = ?)
                                  GROUP BY {currency}, bank_exchange''', (idChat, idChat,))
        other_list_source_tuples = cursor.fetchall()

    deal = {'USD_buys':('покупает', 'USD/BYN'), 'USD_sells':('продает','USD/BYN'),
            'EUR_buys':('покупает', 'EUR/BYN'), 'EUR_sells':('продает','EUR/BYN'),
            'RUB100_buys':('покупает', '100 RUB/BYN'), 'RUB100_sells':('продает','100 RUB/BYN'),
            'EUR_USD_buys':('покупает', 'EUR/USD '), 'EUR_USD_sells':('продает','EUR/USD')}

    formatted_string =  top_list_source_tuples[0][0] [:16] + '         ' + top_list_source_tuples[0][1].upper() + '\n'
    formatted_string += deal.get(currency)[1] + '      '+deal.get(currency)[0] +'  Банк\n'
    formatted_string += ('=' * 30) + '\n'
    for i in range(len(top_list_source_tuples)):
        formatted_string += '{:7.4f}'.format(top_list_source_tuples[i][3])
        formatted_string += '          ' + top_list_source_tuples[i][2] +'\n'
    formatted_string += ('-' * 53) + '\n'
    for i in range(len(other_list_source_tuples)):
        formatted_string += '{:7.4f}'.format(other_list_source_tuples[i][3])
        formatted_string += '          ' + other_list_source_tuples[i][2] +'\n'

    return formatted_string


# функция возращает курсы покупки/продажи банками выбранной валюты
def get_exchange_rates(idChat, currency):
    #list_currency =[]
    curr = {'USD':('USD_buys', 'USD_sells'), 'EUR':('EUR_buys', 'EUR_sells'),
            '100RUB':('RUB100_buys', 'RUB100_sells'), 'EUR/USD':('EUR_USD_buys','EUR_USD_sells')}

    cursor.execute(f'''SELECT date_time, city_bank, bank_exchange, {curr.get(currency)[0]}, {curr.get(currency)[1]}
                              FROM EXCHANGE_RATES
                              LEFT JOIN USERS
                              WHERE EXCHANGE_RATES.city_bank = USERS.city_user
                              AND USERS.idChat = ?
    						  ORDER BY bank_exchange''', (idChat,))
    list_currency = cursor.fetchall()
    formatted_string = list_currency[0][0][:16] + '         ' + list_currency[0][1].upper() + '\n'
    formatted_string += currency + '\nПокупает / Продает           Банк\n'
    formatted_string += ('=' * 30) + '\n'
    for i in range(len(list_currency)):
        formatted_string += '   ' + str(list_currency[i][3]).ljust(6,"0") + ' / ' + str(list_currency[i][4]).ljust(6,"0") + '   ' + list_currency[i][2] +  '\n'

    return formatted_string


# функция возращает адреса/режим работы банков пользователя
def get_addresses(idChat):
    cursor.execute('''SELECT city, bank, address, mode 
                              FROM BANK_CITY
                              LEFT JOIN USERS
                              WHERE city = city_user
                              AND idChat = ?
    						  ORDER BY bank''', (idChat,))

    list_address = cursor.fetchall()
    formatted_string = list_address[0][0].upper() + '\nБанки (адрес, режим работы)\n'
    formatted_string += ('=' * 30) + '\n'
    for i in range(len(list_address)):
        formatted_string += list_address[i][1] + '\n'
        formatted_string += list_address[i][2] + '\n'
        formatted_string += list_address[i][3] + '\n'
        formatted_string += ('-' * 55) + '\n'

    return formatted_string
