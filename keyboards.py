import telebot # импортируем библиотеку
from telebot import types

import datetime

# Функция формирования клавиатуры ReplyKeyboardMarkup
def bottom_keyboard3(bk):
    new_bk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    #bk = ['Вилейка', 'Заславль', 'Мядель', 'Нарочь', 'Радошковичи', 'Воложин', 'Молодечно']
    n = len(bk)
    x = -1
    if n>=3:
        for i in range(n//3):
            new_bk.row(bk[x+1],bk[x+2],bk[x+3])
            x+=3
    if n%3:
        if n%3 == 2:
            new_bk.row(bk[x + 1], bk[x + 2])
        if n % 3 == 1:
            new_bk.row(bk[x + 1])
    return new_bk

# Главная клавиатура
def fun_keyboard_TopCourses(best_courses, cityBank='Молодечно'):
    d = datetime.datetime.now()
    keyboard_TopCourses = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(f'{d.strftime("%d.%m.%Y %H:%M")}    Обновить данные?  Да', callback_data='Обновить данные?')
    keyboard_TopCourses.add(btn1)

    btn2 = telebot.types.InlineKeyboardButton(cityBank, callback_data='Выбрать другой город')
    btn3 = telebot.types.InlineKeyboardButton('Банки покупают', callback_data='Банки покупают')
    btn4 = telebot.types.InlineKeyboardButton('Банки продают', callback_data='Банки продают')
    keyboard_TopCourses.row(btn2, btn3, btn4)

    btn5 = telebot.types.InlineKeyboardButton('USD', callback_data='USD')
    btn6 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[0][1]), callback_data='USD_buys')
    btn7 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[1][1]), callback_data='USD_sells')
    keyboard_TopCourses.row(btn5, btn6, btn7)

    btn8 = telebot.types.InlineKeyboardButton('EUR', callback_data='EUR')
    btn9 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[2][1]), callback_data='EUR_buys')
    btn10 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[3][1]), callback_data='EUR_sells')
    keyboard_TopCourses.row(btn8, btn9, btn10)

    btn11 = telebot.types.InlineKeyboardButton('100RUB', callback_data='100RUB')
    btn12 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[4][1]), callback_data='RUB100_buys')
    btn13 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[5][1]), callback_data='RUB100_sells')
    keyboard_TopCourses.row(btn11, btn12, btn13)

    btn14 = telebot.types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
    btn15 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[6][1]), callback_data='EUR_USD_buys')
    btn16 = telebot.types.InlineKeyboardButton('{:5.4f}'.format(best_courses[7][1]), callback_data='EUR_USD_sells')
    keyboard_TopCourses.row(btn14, btn15, btn16)

    btn17 = telebot.types.InlineKeyboardButton('НацБанк РБ', callback_data='btn17')
    btn18 = telebot.types.InlineKeyboardButton('Банки (адрес, режим работы)', callback_data='адреса')
    keyboard_TopCourses.row(btn17, btn18)

    btn19 = telebot.types.InlineKeyboardButton('Курсы валют всех банков (' + cityBank + ')', callback_data='все банки')
    keyboard_TopCourses.add(btn19)

    return keyboard_TopCourses


























# # Функция формирования нижней клавиатуры ReplyKeyboardMarkup
# def bottom_keyboard3(bk):
#     new_bk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     #bk = ['Вилейка', 'Заславль', 'Молодечно', 'Мядель', 'Нарочь', 'Радошковичи']
#     n = len(bk)
#     x = -1
#     if n>=3:
#         for i in range(n//3):
#             new_bk.row(bk[x+1],bk[x+2],bk[x+3])
#             x+=3
#     if n%3:
#         if n%3 == 2:
#             new_bk.row(bk[x + 1], bk[x + 2])
#         if n % 3 == 1:
#             new_bk.row(bk[x + 1])
#     return new_bk
#
# # # Функция формирования нижней клавиатуры ReplyKeyboardMarkup
# # # bk = ['Да', 'Нет'] - первый аргумент список строк названия кнопок, по умолчанию 'Да', 'Нет'
# # # col = 3 - число колонок клавиатуры, по умолчанию 3
# # # otk =True - убрать клавиатуру после выбора(нажатия кнопки), по умолчанию 'Да'
# # def bottom_keyboard(bk, maxcol = 3, otk =True):
# #     # bk = ['Вилейка', 'Заславль', 'Молодечно', 'Мядель', 'Нарочь', 'Радошковичи']
# #     new_bk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=otk)
# #     n = len(bk)
# #     x = -1
# #     while n:
# #         new_row = []
# #         z = maxcol
# #         while z and n:
# #             if not n: break
# #             x+=1
# #             new_row.append(bk[x])
# #             z-=1
# #             n-=1
# #
# #         # new_row_new = [] # новый список строк
# #         # for s in new_row:  # преобразуем список/список строк в список строк
# #         #     new_row_new.append(''.join(s))
# #
# #         new_bk.row(new_row)
# #     return new_bk
#
# def fun_keyboard_TopCourses(best_courses, cityBank = 'Молодечно' ):
#     d = datetime.datetime.now()
#     keyboard_TopCourses = InlineKeyboardMarkup()
#     btn1 = InlineKeyboardButton(f'{d.strftime("%d.%m.%Y %H:%M")}    Обновить данные?  Да', callback_data='btn1')
#     keyboard_TopCourses.add(btn1)
#
#     btn2 = InlineKeyboardButton(cityBank, callback_data='btn2')
#     btn3 = InlineKeyboardButton('Банки покупают', callback_data='btn3')
#     btn4 = InlineKeyboardButton('Банки продают', callback_data='btn4')
#     keyboard_TopCourses.row(btn2, btn3, btn4)
#
#     btn5 = InlineKeyboardButton('USD', callback_data='btn5')
#     btn6 = InlineKeyboardButton('{:5.4f}'.format(best_courses[0][1]), callback_data='btn6')
#     btn7 = InlineKeyboardButton('{:5.4f}'.format(best_courses[1][1]), callback_data='btn7')
#     keyboard_TopCourses.row(btn5, btn6, btn7)
#
#     btn8 = InlineKeyboardButton('EUR', callback_data='btn8')
#     btn9 = InlineKeyboardButton('{:5.4f}'.format(best_courses[2][1]), callback_data='btn9')
#     btn10 = InlineKeyboardButton('{:5.4f}'.format(best_courses[3][1]), callback_data='btn10')
#     keyboard_TopCourses.row(btn8, btn9, btn10)
#
#     btn11 = InlineKeyboardButton('100RUB', callback_data='btn11')
#     btn12 = InlineKeyboardButton('{:5.4f}'.format(best_courses[4][1]), callback_data='btn12')
#     btn13 = InlineKeyboardButton('{:5.4f}'.format(best_courses[5][1]), callback_data='btn13')
#     keyboard_TopCourses.row(btn11, btn12, btn13)
#
#     btn14 = InlineKeyboardButton('EUR/USD', callback_data='btn14')
#     btn15 = InlineKeyboardButton('{:5.4f}'.format(best_courses[6][1]), callback_data='btn15')
#     btn16 = InlineKeyboardButton('{:5.4f}'.format(best_courses[7][1]), callback_data='btn16')
#     keyboard_TopCourses.row(btn14, btn15, btn16)
#
#     btn17 = InlineKeyboardButton('НацБанк сегодня', callback_data='btn17')
#     btn18 = InlineKeyboardButton('НацБанк на завтра', callback_data='btn18')
#     keyboard_TopCourses.row(btn17, btn18)
#
#     btn19 = InlineKeyboardButton('Курсы валют всех банков (' + cityBank + ')', callback_data='btn19')
#     keyboard_TopCourses.add(btn19)
#
#     return keyboard_TopCourses
#



















#
# button_hi = KeyboardButton('Привет! 👋')
#
# greet_kb = ReplyKeyboardMarkup() # создаём первую клавиатуру
# greet_kb.add(button_hi)          # добавляем в нее кнопку с параметром 'button_hi'
#
# # Создаем новую клавиатуру с параметром resize_keyboard значением True
# greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)
#
# # Создаем новую клавиатуру с кнопкой, котороя после нажатия исчезнит
# greet_kb2 = ReplyKeyboardMarkup(
#     resize_keyboard=True, one_time_keyboard=True
# ).add(button_hi)
#
# # Создаем много кнопок
# button1 = KeyboardButton('1️⃣')
# button2 = KeyboardButton('2️⃣')
# button3 = KeyboardButton('3️⃣')
#
# markup3 = ReplyKeyboardMarkup().add(
#     button1).add(button2).add(button3)
#
# # Создаем кнопки в ряд
# markup4 = ReplyKeyboardMarkup().row(
#     button1, button2, button3
# )
#
# # три ряда
# markup5 = ReplyKeyboardMarkup().row(
#     button1, button2, button3
# ).add(KeyboardButton('Средний ряд'))
#
# button4 = KeyboardButton('4️⃣')
# button5 = KeyboardButton('5️⃣')
# button6 = KeyboardButton('6️⃣')
# markup5.row(button4, button5)
# markup5.insert(button6)
#
# # позволяет запросить у пользователя его контакт или локацию
# markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
#     KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
# ).add(
#     KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
# )
#
# # все методы вместе
# markup_big = ReplyKeyboardMarkup()
#
# markup_big.add(
#     button1, button2, button3, button4, button5, button6
# )
# markup_big.row(
#     button1, button2, button3, button4, button5, button6
# )
#
# markup_big.row(button4, button2)
# markup_big.add(button3, button2)
# markup_big.insert(button1)
# markup_big.insert(button6)
# markup_big.insert(KeyboardButton('9️⃣'))
#
#
# # Инлайн клавиатуры
# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
# inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
# inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
# inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
# inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
# inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
# inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
# inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
# inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
# inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))