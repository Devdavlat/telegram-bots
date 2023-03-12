import telebot
import massages

from telebot.types import BotCommand
from wiki import conf
from environs import Env

env = Env()
env.read_env()

token = env("BOT_TOKEN")
bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start'])
def welcome_mass(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, massages.WELCOME)


@bot.message_handler(commands=['search'])
def welcome_mass(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, massages.SEARCH_TEXT)
    bot.register_next_step_handler_by_chat_id(chat_id, wiki_search_by_text)


def wiki_search_by_text(message):
    text = message.text
    result = conf.WikiManager(text).get_result()
    if result:
        bot.send_message(chat_id=message.chat.id, text=result)
    else:
        bot.send_message(chat_id=message.chat.id, text=massages.TEXT_NOT_FOUND)


def my_commands():
    return [
        BotCommand('/start', 'Boshlash'),
        BotCommand('/search', "Ma'lumot izlash"),

    ]


if __name__ == "__main__":
    print('started ...')
    bot.infinity_polling()
    bot.set_my_commands(my_commands())
