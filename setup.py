# -*- coding: utf-8 -*-
from __init__ import bot
import traceback


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        traceback.print_exc()
        pass


# reply_to_message_id=message.message_id прикрепить сообщение к какому - то сообщению