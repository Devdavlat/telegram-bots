import telebot
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from register_state import StudentRegisterForm
from messages import share_contact_btn, yes_or_no_inline_btn, courser_btn
from environs import Env
from utils import write_csv

env = Env()
env.read_env()
BOT_TOKEN = env('BOT_TOKEN')

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html', state_storage=state_storage)


@bot.message_handler(commands=['start'])
def welcome(message):
    # print('welcome is working')
    bot.send_message(message.from_user.id, '<b>Assalomu alykum.</b>')


@bot.message_handler(commands=['register'])
def start_register(message):
    bot.send_message(message.from_user.id, "Ismingizni kiriting:")
    bot.set_state(message.from_user.id, StudentRegisterForm.name, message.chat.id)


@bot.message_handler(state=StudentRegisterForm.name)
def set_name(message):
    bot.send_message(message.from_user.id, "Familiyangizni kiriting:")
    bot.set_state(message.from_user.id, StudentRegisterForm.surname, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


@bot.message_handler(state=StudentRegisterForm.surname)
def set_surname(message):
    bot.send_message(message.from_user.id, "Yoshingizni kiriing:")
    bot.set_state(message.from_user.id, StudentRegisterForm.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['surname'] = message.text


@bot.message_handler(state=StudentRegisterForm.age)
def set_age(message):
    bot.send_message(message.from_user.id, "Telefon raqamingizni yuboring:", reply_markup=share_contact_btn)
    bot.set_state(message.from_user.id, StudentRegisterForm.contact, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as date:
        date['age'] = message.text


@bot.message_handler(state=StudentRegisterForm.contact, content_types=['contact', 'text'])
def set_contact(message):
    bot.send_message(message.from_user.id, "kursni tanlang", reply_markup=ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, StudentRegisterForm.language, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['contact'] = message.contact.phone_number


@bot.message_handler(state=StudentRegisterForm.language)
def set_language(message):
    bot.send_message(message.from_user.id, 'Tilni kiriting:')
    bot.set_state(message.from_user.id, StudentRegisterForm.course, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['language'] = message.text


@bot.message_handler(state=StudentRegisterForm.course)
def set_course(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['course'] = message.text

    user_data = "<b>Sizning malumotlaringiz:</b>\n"
    user_data += f"<b>Ism :</b> {data.get('name')}\n"
    user_data += f"<b>Familiya :</b> {data.get('surname')}\n"
    user_data += f"<b>Yosh :</b> {data.get('age')}\n"
    user_data += f"<b>Telefon raqam :</b> {data.get('contact')}\n"
    user_data += f"<b>Tanlangan til :</b> {data.get('language')}\n"
    user_data += f"<b>Tanlangan kurs :</b> {data.get('course')}\n"
    user_data += f"<b>Malumotlaringiznmi tekshirib oling</b>"
    bot.send_message(message.from_user.id, user_data, reply_markup=yes_or_no_inline_btn)


@bot.callback_query_handler(lambda call: call.data.startswith('confirm_'))
def set_or_delete_data(call):
    # print('here')
    message = call.message
    data = call.data.split("_")[1]
    with bot.retrieve_data(call.from_user.id, message.chat.id) as d:
        if data == "yes":
            header = list(d.keys())
            write_csv('students.csv', header, d)
            bot.send_message(call.from_user.id, 'Malumotlar saqlanda')
        elif data == 'no':
            bot.send_message(call.from_user.id, 'Malumotlar saqlanmadi /register')
        bot.delete_state(message.from_user.id, message.chat.id)


def my_commands():
    return [
        telebot.types.BotCommand('/start', 'Start bot'),
        telebot.types.BotCommand('/register', "Kursga ro'yxatdan o'tish")
    ]


bot.add_custom_filter(custom_filters.StateFilter(bot))

if __name__ == "__main__":
    print("Started...")
    bot.set_my_commands(my_commands())
    bot.infinity_polling()
