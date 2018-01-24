import telebot as tb
from config import token
from emoji import sos,\
    find,\
    back,\
    restaurant,\
    education,\
    time,\
    transport,\
    plus,\
    question,\
    entertainment,\
    taking_care_of_yourself,\
    health,\
    clothes,\
    recreation,\
    products,\
    graphics,\
    graphics_ ,\
    banknote,\
    house ,\
    present,\
    mount,\
    miscellaneous,\
    sport,\
    calendar,\
    write
from db.redis import set_step_user, \
    get_step_user,\
    set_last_expenses_user,\
    get_last_expenses_user

from db.db_work import registration,\
    set_valuta,\
    set_comment_to_expenses,\
    add_pay,\
    get_pays_month_fpr_pie_diagramm,\
    get_statistic,\
    get_by_categories_pay_month
from messages import message_start,\
    message_set_valute,\
    message_help,\
    message_unknown_command,\
    message_category,\
    message_type_error,\
    message_good_expenses,\
    message_set_comment,\
    message_unknown_error_diagram,\
    message_get_statistic
from view_diagramm import pie_diagram
import os
import traceback
from write_to_xls import file,file_categories
import binascii

today = 'сегодня'
week = "неделю"
month = 'месяц'
year = "год"


user_markup_default = tb.types.ReplyKeyboardMarkup(False, True, True)
user_markup_default.row(products, education, taking_care_of_yourself, entertainment,sport)
user_markup_default.row( health, restaurant, transport, clothes,recreation, house, present)
user_markup_default.row(graphics_,  sos)

LENGTH_CONTENT = 5000


bot = tb.TeleBot(token)


@bot.message_handler(commands=['start'])
def handler_text(message):
    registration(message.from_user.id,message.chat.first_name,message.chat.last_name)
    bot.send_sticker(message.from_user.id,
                     'CAADAgADQgADGgZFBJvaLJpbpAXhAg')
    bot.send_message(message.from_user.id,
                     message_start.format(message.chat.first_name))
    set_step_user(message.from_user.id, 1)
                     # reply_markup=user_markup_default)


@bot.message_handler(content_types=['text'])
def handler_text(message):

    def get_command_by_step(step):
        if step == 30:
            message_text_answer = 'продукты' + products
        elif step == 40:
            message_text_answer = 'образование' + education
        elif step == 50:
            message_text_answer = 'уход за собой' + taking_care_of_yourself
        elif step == 60:
            message_text_answer = 'развлечения' + entertainment
        elif step == 70:
            message_text_answer = 'спорт' + sport
        elif step == 80:
            message_text_answer = 'здоровье' + health
        elif step == 90:
            message_text_answer = 'кафе/ресторан' + restaurant
        elif step == 100:
            message_text_answer = 'транспорт' + transport
        elif step == 110:
            message_text_answer = 'одежда' + clothes
        elif step == 120:
            message_text_answer = 'отдых' + recreation
        elif step == 130:
            message_text_answer = 'дом' + house
        elif step == 140:
            message_text_answer = 'подарки' + present
        return message_text_answer

    def command(text):
        # products, education, taking_care_of_yourself, entertainment
        # sport,health,restaurant,transport,clothes
        # recreation,house,present
        message_text_answer = ''
        answer = True
        if text == products:
            message_text_answer = 'продукты' + products
            code_step = 30
        elif text == education:
            message_text_answer = 'образование' + education
            code_step = 40
        elif text == taking_care_of_yourself:
            message_text_answer = 'уход за собой' + taking_care_of_yourself
            code_step = 50
        elif text == entertainment:
            message_text_answer = 'развлечения' + entertainment
            code_step = 60
        elif text == sport:
            message_text_answer = 'спорт' + sport
            code_step = 70
        elif text == health:
            message_text_answer = 'здоровье' + health
            code_step = 80
        elif text == restaurant:
            message_text_answer = 'кафе/ресторан' + restaurant
            code_step = 90
        elif text == transport:
            message_text_answer = 'транспорт' + transport
            code_step = 100
        elif text == clothes:
            message_text_answer = 'одежда' + clothes
            code_step = 110
        elif text == recreation:
            message_text_answer = 'отдых' + recreation
            code_step = 120
        elif text == house:
            message_text_answer = 'дом' + house
            code_step = 130
        elif text == present:
            message_text_answer = 'подарки' + present
            code_step = 140
        else:
            answer = False
            code_step = 2
        return answer,\
               code_step,\
               message_text_answer

    if message.text == back:
        set_step_user(message.from_user.id, 2)
        bot.send_message(message.from_user.id,
                         'вы вернулись к началу',
                         reply_markup=user_markup_default)
        return

    step = get_step_user(message.from_user.id)
    if step == 1:
        set_valuta(message.from_user.id, message.text)
        set_step_user(message.from_user.id, 2)
        bot.send_message(message.from_user.id,
                         message_set_valute.format(message.chat.first_name, message.text),
                         reply_markup=user_markup_default)

    elif step == 2:

        if message.text == graphics_:
            cat = get_pays_month_fpr_pie_diagramm(message.from_user.id)
            # print(cat)
            try:
                data = get_by_categories_pay_month(message.from_user.id)
                name = (str(binascii.hexlify(os.urandom(20)))[2:42])
                path = file_categories(data,name)
                bot.send_document(message.from_user.id, open(path, 'rb'))
                name_file = pie_diagram(cat)
                # print(name_file)
                # bot.send_photo(message.from_user.id, open(name_file, 'rb'))
                bot.send_photo(message.from_user.id, open(name_file, 'rb'))
                # os.remove(os.getcwd() + '/' +name_file)
            except:
                traceback.print_exc()
                bot.send_sticker(message.from_user.id,
                                 'CAADAgADigADGgZFBHF3_01Pcn2FAg')
                bot.send_message(message.from_user.id,
                                 message_unknown_error_diagram.format(message.chat.first_name))

        elif message.text == miscellaneous:
            pass
        elif message.text == sos:
            bot.send_sticker(message.from_user.id,
                             'CAADAgADegADGgZFBLEHj54VZGIgAg')

            bot.send_message(message.from_user.id,
                             message_help.format(message.chat.first_name),
                             reply_markup=user_markup_default)
        else:
            res, code_step, message_answer = command(message.text)
            if res:
                set_step_user(message.from_user.id, code_step)
                user_markup = tb.types.ReplyKeyboardMarkup(True, True, True)
                user_markup.row(back, calendar)

                bot.send_message(message.from_user.id,
                                 message_category.format(message.chat.first_name,
                                                         message_answer),
                                 parse_mode='Markdown',
                                 reply_markup=user_markup)
            else:
                bot.send_message(message.from_user.id,
                                 message_unknown_command.format(message.chat.first_name))
    else:
        if step % 10 == 0:
            try:
                pay = round(abs(float(message.text.replace(',', '.'))),2)
                if pay < 1000000:
                    id_expenses = add_pay(message.from_user.id, pay, int(step / 10))
                    set_last_expenses_user(message.from_user.id, id_expenses)
                    set_step_user(message.from_user.id, step+1)
                    bot.send_message(message.from_user.id,
                                     message_set_comment.format(message.chat.first_name))
                else:
                    bot.send_sticker(message.from_user.id,
                                     'CAADAgADVAADGgZFBHo9RTRiHBZ-Ag')
                    bot.send_message(message.from_user.id,
                                     '{}, я тебе не верю! '.format(message.chat.first_name))

            except TypeError:
                bot.send_message(message.from_user.id,
                                 message_type_error.format(message.chat.first_name))
            except ValueError:
                if message.text == calendar:
                    set_step_user(message.from_user.id, int(step/10) * 10 + 9)
                    user_markup = tb.types.ReplyKeyboardMarkup(True, True, True)
                    user_markup.row(today,week)
                    user_markup.row(month, year)
                    user_markup.row(back, write)
                    bot.send_message(message.from_user.id,
                                     message_get_statistic.format(message.chat.first_name),
                                     reply_markup=user_markup)

                else:
                    bot.send_message(message.from_user.id,
                                     message_type_error.format(message.chat.first_name))
        elif step % 10 == 1:
            id_expenses = get_last_expenses_user(message.from_user.id)
            set_step_user(message.from_user.id, 2)
            set_comment_to_expenses(id_expenses, message.text)
            bot.send_message(message.from_user.id,
                             message_good_expenses.format(message.chat.first_name),
                             reply_markup=user_markup_default)

        elif step %10 == 9:
            if message.text == today:
                period = 'day'
                name = (str(binascii.hexlify(os.urandom(20)))[2:42])
                data, sum_ = get_statistic(message.from_user.id, int(step /10), period)
                path_to_file = file(data, today, name)
                bot.send_document(message.from_user.id, open(path_to_file, 'rb'))
                bot.send_message(message.from_user.id,
                                 '{}, за текущий день вы поторатили: *{}*'.format(message.chat.first_name, sum_),
                                 parse_mode='Markdown')
            elif message.text == week:
                period = 'week'
                name = (str(binascii.hexlify(os.urandom(20)))[2:42])
                data, sum_ = get_statistic(message.from_user.id, int(step / 10), period)
                path_to_file = file(data, week, name)
                bot.send_document(message.from_user.id, open(path_to_file, 'rb'))
                bot.send_message(message.from_user.id,
                                 '{}, за текущую неделю вы поторатили: *{}*'.format(message.chat.first_name, sum_),
                                 parse_mode='Markdown')
            elif message.text == month:
                period = 'month'
                name = (str(binascii.hexlify(os.urandom(20)))[2:42])
                data, sum_ = get_statistic(message.from_user.id, int(step / 10), period)
                path_to_file = file(data, month, name)
                bot.send_document(message.from_user.id, open(path_to_file, 'rb'))
                bot.send_message(message.from_user.id,
                                 '{}, за  текущий месяц вы поторатили: *{}*'.format(message.chat.first_name, sum_),
                                 parse_mode='Markdown')
            elif message.text == year:
                period = 'year'
                name = (str(binascii.hexlify(os.urandom(20)))[2:42])
                data, sum_ = get_statistic(message.from_user.id, int(step / 10), period)
                path_to_file = file(data, year, name)
                bot.send_document(message.from_user.id, open(path_to_file, 'rb'))
                bot.send_message(message.from_user.id,
                                 '{}, за текущий год  вы поторатили: *{}*'.format(message.chat.first_name,sum_),
                                 parse_mode='Markdown')
            elif message.text == write:
                message_answer = get_command_by_step(int(step/10) * 10)
                set_step_user(message.from_user.id, int(step/10) * 10)
                user_markup = tb.types.ReplyKeyboardMarkup(True, True, True)
                user_markup.row(back, calendar)

                bot.send_message(message.from_user.id,
                                 message_category.format(message.chat.first_name,
                                                         message_answer),
                                 parse_mode='Markdown',
                                 reply_markup=user_markup)
            else:
                bot.send_message(message.from_user.id,
                                 message_unknown_command.format(message.chat.first_name))








