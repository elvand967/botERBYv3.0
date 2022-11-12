# Что может делать этот бот?
# Этот бот представляет актуальную информацию, из доступных интернет источников,
# о курсах обмена иностранной валюты в коммерческих банках избранного населенного пункта Республики Беларусь.
# Адреса подразделений банков и график их работы.
# Делает выборку банков с лучшими курсами обмена (покупать дешевле – продавать дороже),
# предоставляет отдельные сведения о покупке или продаже банками валюты,
# а также информацию по выбранной иностранной валюте у коммерческих банков населенного пункта.
# Официальный курс белорусского рубля к избранным иностранным валютам
# Национального Банка Республики Беларусь в режиме сегодня/завтра.
# Для запуска бота напишите сообщение: Привет
# или же команду: /start
# You will find it at       t.me/ExchangeRates_By_bot
# developer :
# telegram: dubanevich_vk
# twitter:  @d_vladimir


import telebot  # импортируем библиотеку
from telebot import types
# import datetime
from config import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

import keyboards as kb
import database as db


# Проверим наличие, при необходимости создадим нужные таблицы базы данных бота
if not db.fun_checking_if_table_exists('USERS'):
    db.fun_table_users()  # создание таблицы пользователи
if not db.fun_checking_if_table_exists('BANK_CITY'):
    db.fun_table_bank_city()  # создание таблицы всех банков городов и заполнение
if not db.fun_checking_if_table_exists('BANK_CITY_USERS'):
    db.fun_table_bank_city_users()  # создание таблицы городов-банков для ID.пользователя
if not db.fun_checking_if_table_exists('EXCHANGE_RATES'):  # курсы валют
    db.fun_table_exchange_rates()

print('start bot')
mesID = []

# обработчик, который при команде /start, будет отправлять нам сообщение и наш шаблон
@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.delete_message(message.chat.id, message.id)  # удалим сообщение пользователя
    # по умолчанию зарегистрируем пользователя, с пропиской user_city = 'Молодечно'
    # и url_user = 'https://myfin.by/currency/molodechno'
    db.fun_reg_user(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username,
                    message.chat.type)
    db.fun_set_bank_city_users(
        message.chat.id)  # зарегестрируем банки города пользователя (временно Молодечно, а там как будет)
    db.fun_set_courses(message.chat.id)  # функция загрузки/обновления курсов
    msg = 'Привет! 👋\nВас интересуют курсы обмена валют в коммерческих банках\nг. Молодечно?\n(Вы в любой момент можете изменить населенный пункт,\n' \
          'нажав кнопку (Молодечно, Вилейка и т.п.) главного меню.)'
    question_city = ['Да, Молодечно', 'Нет, выбрать другой город']
    global mesID
    mesID.append(bot.send_message(message.chat.id, msg, reply_markup=kb.bottom_keyboard3(question_city)))


# @bot.message_handler(commands=['0'])
# def start_message(message):
#     msg = 'Привет! 👋\nВас интересуют курсы обмена валют в коммерческих банках\nг. Молодечно?\n(Вы в любой момент можете изменить населенный пункт,\n' \
#           'нажав кнопку (Молодечно, Вилейка и т.п.) главного меню.)'
#     question_city = ['Да, Молодечно', 'Нет, выбрать другой город']
#     bot.send_message(message.chat.id, msg, reply_markup=kb.bottom_keyboard3(question_city))


@bot.message_handler(content_types=['text'])
def echo(message):
    # cities = db.fun_get_cities()  # доступные города в БД
    cities = ['Вилейка', 'Воложин', 'Заславль', 'Мядель', 'Нарочь', 'Радошковичи', 'Молодечно']
    global mesID
    if message.text.capitalize()[:6] == 'Привет':
        # по умолчанию зарегистрируем пользователя, с пропиской user_city = 'Молодечно'
        # и url_user = 'https://myfin.by/currency/molodechno'
        db.fun_reg_user(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username,
                        message.chat.type)
        db.fun_set_bank_city_users(
            message.chat.id)  # зарегестрируем банки города пользователя (временно Молодечно, а там как будет)
        db.fun_set_courses(message.chat.id)  # функция загрузки/обновления курсов
        msg = 'Привет! 👋\nВас интересуют курсы обмена валют в коммерческих банках\nг. Молодечно?\n(Вы в любой момент можете изменить населенный пункт,\n' \
              'нажав кнопку (Молодечно, Вилейка и т.п.) главного меню.)'
        question_city = ['Да, Молодечно', 'Нет, выбрать другой город']
        global mesID
        mesID.append(bot.send_message(message.chat.id, msg, reply_markup=kb.bottom_keyboard3(question_city)))

    elif message.text == 'Да, Молодечно':

        if len(mesID):
            for mes in mesID:
                bot.delete_message(message.chat.id, mes.id)
            mesID = []

        db.fun_set_user_city_update(message.chat.id, 'Молодечно')  # функция регистрации изменения города пользователя.
        db.fun_set_bank_city_users(message.chat.id)  # функция заполнения таблицы  банков города ID.пользователя
        db.fun_set_courses(message.chat.id)  # функция загрузки/обновления курсов
        bot.send_message(message.chat.id, 'Главная\nЛучшие курсы валют в коммерческих банках г.Молодечно',
                         reply_markup=kb.fun_keyboard_TopCourses(db.fun_best_courses(message.chat.id)))

    elif message.text == 'Нет, выбрать другой город':  # or message.text == 'Выбрать другой город' :

        if len(mesID):
            for mes in mesID:
                bot.delete_message(message.chat.id, mes.id)
            mesID = []

        # вызываем ReplyKeyboardMarkup клавиатуру с доступными городами
        bot.send_message(message.chat.id, 'Выберите нужный населенный пункт:', reply_markup=kb.bottom_keyboard3(cities))

    elif message.text in cities:  # пользователь выбрал один из городов имеющихся в БД
        db.fun_set_user_city_update(message.chat.id, message.text)  # функция регистрации изменения города пользователя.
        db.fun_set_bank_city_users(message.chat.id)  # функция заполнения таблицы  банков города ID.пользователя
        db.fun_set_courses(message.chat.id)  # функция загрузки/обновления курсов
        bot.send_message(message.chat.id, 'Главная\nЛучшие курсы валют в коммерческих банках (' + message.text + ')'
                         , reply_markup=kb.fun_keyboard_TopCourses(db.fun_best_courses(message.chat.id),
                                                                   db.fun_get_city_user(message.chat.id)))

    else:
        bot.send_message(message.chat.id, (message.text + '?      Я тебя не понимаю'))  # эхо

    bot.delete_message(message.chat.id, message.id)  # удалим сообщение пользователя
    # bot.delete_message(message.chat.id, message.message.id)  # удалим все сообщения - ???


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    # bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за выбор!') # всплывающая подсказка
    # answer = ''
    currencies = ['USD', 'EUR', '100RUB', 'EUR/USD']

    if call.data == 'Обновить данные?':
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback. В том числе клавиатуру!!!
        img = open(db.fun_image_file_name(), 'rb')
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=img,
            caption='')
        advertising = telebot.types.InlineKeyboardMarkup()
        advertising.row(telebot.types.InlineKeyboardButton(text='Отключить', callback_data='Отключить'),
                        telebot.types.InlineKeyboardButton(text='Добавить', callback_data='Добавить'))
        # advertising.add(telebot.types.InlineKeyboardButton(text='Добавить', callback_data='Добавить'))
        bot.send_message(call.message.chat.id, 'Рекламный блок Telegram chat', reply_markup=advertising)
        # -------------------------------------------------------------
        city = db.fun_get_city_user(call.message.chat.id)
        answer = 'Главная\nЛучшие курсы валют в коммерческих банках (' + city + ')'
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # удаление клавиатуры после выбора
        db.fun_set_courses(call.message.chat.id)  # функция загрузки/обновления курсов
        bot.send_message(call.message.chat.id, answer
                         , reply_markup=kb.fun_keyboard_TopCourses(db.fun_best_courses(call.message.chat.id), city))

    elif call.data == 'Выбрать другой город':
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback!!!
        cities = ['Вилейка', 'Воложин', 'Заславль', 'Мядель', 'Нарочь', 'Радошковичи', 'Молодечно']
        answer = 'Изменить населенный пункт'
        bot.send_message(call.message.chat.id, answer, reply_markup=kb.bottom_keyboard3(cities))

    elif call.data == 'все банки':  # вывод курсов валют всех банков города
        answer = db.fun_form_all_courses(call.message.chat.id)
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback. В том числе клавиатуру!!!
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # удаление клавиатуры после выбора

        open_home = telebot.types.InlineKeyboardMarkup()
        open_home.add(telebot.types.InlineKeyboardButton(text='Открыть главнyю', callback_data='Открыть главнyю'))
        bot.send_message(call.message.chat.id, answer, reply_markup=open_home)

    elif call.data == 'Открыть главнyю':  # Открыть главнyю форму - лучшие курсы
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback. В том числе клавиатуру!!!
        city = db.fun_get_city_user(call.message.chat.id)
        answer = 'Главная\nЛучшие курсы валют в коммерческих банках (' + city + ')'
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # удаление клавиатуры после выбора
        db.fun_set_courses(call.message.chat.id)  # функция загрузки/обновления курсов
        bot.send_message(call.message.chat.id, answer
                         , reply_markup=kb.fun_keyboard_TopCourses(db.fun_best_courses(call.message.chat.id), city))

    elif call.data.find('buys') != -1:  # Открыть сведения о банке с лучшими курсами покупки
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback. В том числе клавиатуру!!!

        answer = db.get_top_buys(call.message.chat.id, call.data)
        open_home = telebot.types.InlineKeyboardMarkup()
        open_home.add(telebot.types.InlineKeyboardButton(text='Открыть главнyю', callback_data='Открыть главнyю'))
        bot.send_message(call.message.chat.id, answer, reply_markup=open_home)

    elif call.data.find('sells') != -1:  # Открыть сведения о банке с лучшими курсами продажи
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback. В том числе клавиатуру!!!

        answer = db.get_top_buys(call.message.chat.id, call.data)
        open_home = telebot.types.InlineKeyboardMarkup()
        open_home.add(telebot.types.InlineKeyboardButton(text='Открыть главнyю', callback_data='Открыть главнyю'))
        bot.send_message(call.message.chat.id, answer, reply_markup=open_home)

    elif call.data in currencies:  # Открыть сведения о валюте покупаемой/ продоваемой банками
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback. В том числе клавиатуру!!!

        answer = db.get_exchange_rates(call.message.chat.id, call.data)
        open_home = telebot.types.InlineKeyboardMarkup()
        open_home.add(telebot.types.InlineKeyboardButton(text='Открыть главнyю', callback_data='Открыть главнyю'))
        bot.send_message(call.message.chat.id, answer, reply_markup=open_home)

    elif call.data == 'адреса':  # вывод адресов всех банков города
        answer = db.get_addresses(call.message.chat.id)
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)  # удалим все сообщения бота отправленные из - callback. В том числе клавиатуру!!!
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)  # удаление клавиатуры после выбора

        open_home = telebot.types.InlineKeyboardMarkup()
        open_home.add(telebot.types.InlineKeyboardButton(text='Открыть главнyю', callback_data='Открыть главнyю'))
        bot.send_message(call.message.chat.id, answer, reply_markup=open_home)


#
# @dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
# async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
#     code = callback_query.data[-1]
#     if code.isdigit():
#         code = int(code)
#     if code == 2:
#         await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
#
#     elif code == 5:
#         await bot.answer_callback_query(
#             callback_query.id,
#             text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
#     else:
#         await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)