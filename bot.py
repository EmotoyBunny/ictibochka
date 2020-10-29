# -*- coding: utf-8 -*-

import os
import telebot
from telebot import types
from flask import Flask, request
import config
import requests
import json 
import datetime

bot = telebot.TeleBot(config.token)
server = Flask(__name__)
TOKEN = config.token

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_menu.row('Расписание группы \U0001F4D2')
markup_menu.row('Собственное расписание \U0001F4DD')
markup_menu.row('Информация о вузе \U0001F4A1')
markup_menu.row('Настройки \u2692')

markup_schedule = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_schedule.row('Сегодня', 'Завтра')
markup_schedule.row('Понедельник', 'Вторник', 'Среда')
markup_schedule.row('Четверг', 'Пятница', 'Суббота')
markup_schedule.row('Назад \u21a9\ufe0f')

markup_info = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_info.row('Основные сайты \U0001F4CC')
markup_info.row('Группы Вконтакте \U0001F4CC')
markup_info.row('Информация о корпусах \U0001F3E3')
markup_info.row('Назад \u21a9\ufe0f')

markup_corps = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_corps.row('Корпус А', 'Корпус Б', 'Корпус В', 'Корпус Г')
markup_corps.row('Корпус Д','Корпус Е','Корпус И','Корпус К',)
markup_corps.row('Назад \u21a9\ufe0f')

def gen_markup():
   markup = types.InlineKeyboardMarkup()
   markup.row_width = 3
   markup.add(types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
            types.InlineKeyboardButton("No", callback_data="cb_no1"),
            types.InlineKeyboardButton("No", callback_data="cb_no2"),
            types.InlineKeyboardButton("No", callback_data="cb_no3"),
            types.InlineKeyboardButton("No", callback_data="cb_no4"),
            types.InlineKeyboardButton("No", callback_data="cb_no5"))
   return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, "Добро пожаловать, введите группу (Например КТбо2-3)")
    bot.register_next_step_handler(msg, reg_user)

def reg_user(message):
    url = "http://ictib.host1809541.hostland.pro/index.php/api/reg_user"
    print(message.text)
    params = dict(
       user_id=message.from_user.id,
       user_group=message.text
    )
    resp = requests.get(url=url, params=params)
    print(resp.content)
    binary = resp.content
    data = json.loads(binary)

    chat_id = message.chat.id

    if data['success'] == 'true':
        text = 'Вы записаны \u2714\ufe0f'
        bot.send_message(chat_id, text, reply_markup=markup_menu)
    elif data['success'] == 'false':
        msg = bot.reply_to(message, "Некорректный ввод.\nПовторите попытку")
        bot.register_next_step_handler(msg, reg_user)
    else:
        bot.send_message(message.chat.id, "Вы уже записаны \u2714\ufe0f", reply_markup=markup_menu)

@bot.message_handler(content_types=['text'])
def handle_text(message):
   global group
   group = "Неизвестно"
   group = get_user_group(message.from_user.id)
   if message.text == "Расписание группы \U0001F4D2":
      get_week_schedule(message.from_user.id)
      bot.send_message(message.chat.id, "Выберите день", reply_markup=markup_schedule)
   elif message.text == "Информация о вузе \U0001F4A1":
      bot.send_message(message.chat.id, "Какая информация вам инетересна?", reply_markup=markup_info)
   elif message.text == "Информация о корпусах \U0001F3E3":
      bot.send_message(message.chat.id, "Выберете корпус", reply_markup=markup_corps)
   elif message.text == "Сегодня":
      day = get_day_of_week(True)
      text = get_schedule(day, message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule)
   elif message.text == "Завтра":
      day = get_day_of_week(False)
      text = get_schedule(day, message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule)
   elif message.text == "Понедельник":
      text = get_schedule('Пнд', message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule)
   elif message.text == "Вторник":
      text = get_schedule('Втр', message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule) 
   elif message.text == "Среда":
      text = get_schedule('Срд', message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule)
   elif message.text == "Четверг":
      text = get_schedule('Чтв', message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule)
   elif message.text == "Пятница":
      text = get_schedule('Птн', message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule)
   elif message.text == "Суббота":
      text = get_schedule('Сбт', message.from_user.id)
      bot.send_message(message.chat.id, text, reply_markup=markup_schedule)
   elif message.text == "Основные сайты \U0001F4CC":
      keyboard = types.InlineKeyboardMarkup()
      url_button1 = types.InlineKeyboardButton(text="Личный кабинет студента", url="https://www.sfedu.ru/www/stat_pages22.show?p=STD/lks/D")
      url_button2 = types.InlineKeyboardButton(text="LMS", url="https://lms.sfedu.ru")
      url_button3 = types.InlineKeyboardButton(text="БРС", url="https://grade.sfedu.ru/")
      url_button4 = types.InlineKeyboardButton(text="Сайт ИКТИБа", url="http://ictis.sfedu.ru/")
      url_button5 = types.InlineKeyboardButton(text="Проектный офис ИКТИБ", url="https://proictis.sfedu.ru/")
      keyboard.add(url_button1, url_button2, url_button3, url_button4, url_button5)
      bot.send_message(message.chat.id, "Что вас инетересует?", reply_markup=keyboard)
   elif message.text == "Группы Вконтакте \U0001F4CC":
      keyboard = types.InlineKeyboardMarkup()
      keyboard.row_width = 1
      url_button1 = types.InlineKeyboardButton(text="Физическая культура в ИТА ЮФУ", url="https://vk.com/club101308251")
      url_button2 = types.InlineKeyboardButton(text="Подслушано в ЮФУ", url="https://vk.com/overhearsfedu")
      url_button3 = types.InlineKeyboardButton(text="ИКТИБ ЮФУ", url="https://vk.com/ictis_sfedu")
      url_button4 = types.InlineKeyboardButton(text="Студенческий клуб ИТА ЮФУ (г. Таганрог)", url="https://vk.com/studclub_tgn")
      url_button5 = types.InlineKeyboardButton(text="Студенческий киберспортивный клуб ЮФУ", url="https://vk.com/esports_sfedu")
      url_button6 = types.InlineKeyboardButton(text="Культура здоровья в ИТА ЮФУ", url="https://vk.com/club150688847")
      url_button7 = types.InlineKeyboardButton(text="Первокурснику", url="https://vk.com/1kurs_ita_2019")
      url_button8 = types.InlineKeyboardButton(text="Технологии + Проекты + Инновации ИКТИБ", url="https://vk.com/proictis")
      url_button9 = types.InlineKeyboardButton(text="Волонтерский центр ИКТИБ ЮФУ", url="https://vk.com/ictis_vol")
      keyboard.add(url_button1, url_button2, url_button3, url_button4, url_button5, url_button6, url_button7, url_button8, url_button9)
      bot.send_message(message.chat.id, "Что вас инетересует?", reply_markup=keyboard)
   elif message.text == "Корпус А":
      text = "Таганрог, улица Чехова, 22"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.205446", longitude="38.938832")
   elif message.text == "Корпус Б":
      text = "Таганрог, улица Чехова, 22"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.205396", longitude="38.938842")
   elif message.text == "Корпус В":
      text = "Таганрог, ул. Петровская, 81"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.216498", longitude="38.926859")
   elif message.text == "Корпус Г":
      text = "Таганрог, Некрасовский переулок, 42"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.203241", longitude="38.934853")
   elif message.text == "Корпус Д":
      text = "Таганрог, Некрасовский переулок, 44"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.205446", longitude="38.938832")
   elif message.text == "Корпус Е":
      text = "Таганрог, ул. Шевченко, 2"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.204446", longitude="38.944437")
   elif message.text == "Корпус И":
      text = "Таганрог, улица Чехова, 2"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.203932", longitude="38.943927")
   elif message.text == "Корпус К":
      text = "Таганрог, ул. Шевченко, 2"
      bot.send_message(message.chat.id, text, reply_markup=markup_corps)
      bot.send_location(message.chat.id, latitude="47.204446", longitude="38.944437")
   elif message.text == "Настройки \u2692":
      markup_config = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup_config.row("\U0001F527 Группа: {}".format(group))
      markup_config.row("Назад \u21a9\ufe0f ")
      text = "Настройки \u2692"
      bot.send_message(message.chat.id, text, reply_markup=markup_config)
   elif message.text == "\U0001F527 Группа: {}".format(group):
      msg = bot.send_message(message.chat.id, "Введите группу (Пример КТбо2-3)")
      bot.register_next_step_handler(msg, change_group)
   elif message.text == "Собственное расписание \U0001F4DD":
      bot.send_message(message.chat.id, "Выберите день", reply_markup=gen_markup())
      # if message.text == "Пнд":
      #    bot.send_message(message.chat.id, "Выберите пару", reply_markup=markup_user_schedule_pair_count)
   elif message.text == "Назад \u21a9\ufe0f":
      bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=markup_menu)
   else:
      bot.send_message(message.chat.id, "\u274c Некорректный ввод")

def change_group(message):
    url = "http://ictib.host1809541.hostland.pro/index.php/api/change_user_group"
    print(message.text)
    params = dict(
       user_id=message.from_user.id,
       user_group=message.text
    )
    resp = requests.get(url=url, params=params)
    print(resp.content)
    binary = resp.content
    data = json.loads(binary)

    chat_id = message.chat.id

    if data['success'] == 'true':
        global group
        text = 'Группа была изменена'
        group = message.text
        markup_config = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_config.row("\U0001F527 Группа: {}".format(group))
        markup_config.row("Назад  \u21a9\ufe0f")
        bot.send_message(chat_id, text, reply_markup=markup_config)
    elif data['success'] == 'false':
        msg = bot.reply_to(message, "\u274c Некорректный ввод")
        bot.register_next_step_handler(msg, change_group)
    else:
        msg = bot.reply_to(message, "\u2b55\ufe0f Группа уже указана")
        bot.register_next_step_handler(msg, change_group)


def get_week_schedule(user_id):
    url = "http://ictib.host1809541.hostland.pro/index.php/api/get_week_schedule"
    params = dict(
        user_id=user_id
    )
    resp = requests.get(url=url, params=params)
    return resp.content

def get_schedule(day, user_id):
   schedule = []
   pair_list = []
   url = "http://ictib.host1809541.hostland.pro/index.php/api/get_day_schedule"
   params = dict(
      day=day,
      user_id=user_id
   )
   resp = requests.get(url=url, params=params)
   print(resp.content)
   binary = resp.content
   data = json.loads(binary)
   for idx, pair in enumerate(data['pairs'], start=0):
      del pair_list[:]
      if pair['pair_name']:
         pair_list.append("\U0001F514 Пара №{}: {} \n".format(idx+1, pair['time']))
         pair_list.append(pair['pair_name'] + '\n\n')
      else:
         pair_list.append("\U0001F515 Пара №{}: Окно \n\n".format(idx+1))
      print(pair_list)
      schedule.append(pair_list[:])
      print(schedule)
   print(schedule)
   text = ''

   for schedules in schedule:
      text += '' + ''.join(schedules)
   
   text = "\U0001F4C5 Дата - {}\n\U0001F534Неделя - {}\n\n{}".format(data['day'], data['week'], text)

   # data = json.dumps(data) 
   return text

def get_day_of_week(today):
   day = datetime.datetime.today().weekday()+1
   print(datetime.datetime.today())
   print(day)
   if not today:
      day += 1
   if day == 1:
      print('Пнд')
      return 'Пнд'
   elif day == 2:
      print('Втр')
      return 'Втр'
   elif day == 3:
      print('Срд')
      return 'Срд'
   elif day == 4:
      print('Чтв')
      return 'Чтв'
   elif day == 5:
      print('Птн')
      return 'Птн'   
   elif day == 6:
      print('Сбт')
      return 'Сбт' 
   else:
      print('undefined')
      return 'Пнд'

def get_user_group(user_id):
   url = "http://ictib.host1809541.hostland.pro/index.php/api/get_info"
   params = dict(
      user_id=user_id
   )
   resp = requests.get(url=url, params=params)
   binary = resp.content
   print(binary)
   data = json.loads(binary)
   user_group = data['user_group']
   return user_group

# SERVER SIDE 
@server.route('/' + config.token, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://calm-refuge-95446.herokuapp.com/' + TOKEN)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

# if __name__ == '__main__':
#     bot.polling(none_stop=True)