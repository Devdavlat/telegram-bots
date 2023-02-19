import telebot
from environs import Env
import messages
import utils
import keyboards
from trello import TrelloManager
from states import CreateNewTask

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    print('welcome is working')
    bot.send_message(message.chat.id, messages.WELCOME_START_COMMAND)


@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.from_user.id, messages.CANCEL)


@bot.message_handler(commands=['register'])
def username_registration(message):
    if not utils.check_chat_id_from_csv('chat.csv', message.from_user.id):
        bot.send_message(message.from_user.id, messages.SEND_USERNAME)
        bot.register_next_step_handler(message, get_trello_username)
    else:
        bot.send_message(message.from_user.id, messages.ALREADY_EXIST)


def get_trello_username(message):
    utils.write_chat_csv('chat.csv', message)
    bot.send_message(message.from_user.id, messages.ADD_SUCCESSFULLY)


@bot.message_handler(commands=['boards'])
def get_boards(message):
    if not utils.check_chat_id_from_csv('chat.csv', message.from_user.id):
        bot.send_message(message.from_user.id, messages.TRELLO_USERNAME_NOT_FOUND)
    else:
        trello_username = utils.get_trello_username_by_chat_id('chat.csv', message.from_user.id)
        if trello_username:
            bot.send_message(
                message.from_user.id,
                messages.SELECT_BOARD,
                reply_markup=keyboards.get_inline_boards_btn(trello_username, "show_tasks")
            )
        else:
            bot.send_message(message.from_user.id, messages.TRELLO_USERNAME_NOT_FOUND)


@bot.callback_query_handler(lambda call: call.data.startswith("show_tasks_"))
def get_board_list(call):
    message = call.message
    trello_username = utils.get_trello_username_by_chat_id('chat.csv', message.from_user.id)
    trello = TrelloManager(trello_username)
    board_id = call.data.split("_")[2]
    bot.send_message(
        call.from_user.id,
        messages.SELECT_LIST,
        reply_markup=keyboards.get_inline_list_btn(trello, board_id, "show_list_tasks")
    )


@bot.callback_query_handler(lambda call: call.data.startswith("show_list_tasks"))
def get_member_cards(call):
    message = call.message
    list_id = call.data.split("_")[3]
    trello_username = utils.get_trello_username_by_chat_id('chat.csv', message.chat.id)
    trello = TrelloManager(trello_username)
    card_data = trello.get_cards_on_a_list(list_id)
    msg = utils.get_members_task_messages(card_data, trello.get_member_id())
    if msg:
        bot.send_message(call.from_user.id, msg, parse_mode='html')
    else:
        bot.send_message(call.from_user.id, messages.NO_TASKS)


@bot.message_handler(commands=['new'])
def create_new_task(message):
    if not utils.check_chat_id_from_csv('chat.csv', message.from_user.id):
        bot.send_message(message.from_user.id, messages.TRELLO_USERNAME_NOT_FOUND)
    else:
        trello_username = utils.get_trello_username_by_chat_id('chat.csv', message.from_user.id)

        if trello_username:
            bot.send_message(
                message.from_user.id,
                messages.CREATE_TASK,
                reply_markup=keyboards.get_inline_boards_btn(trello_username, "newtask")
            )
            bot.set_state(message.from_user.id, CreateNewTask.board, message.chat.id)
        else:
            bot.send_message(message.from_user.id, messages.TRELLO_USERNAME_NOT_FOUND)


@bot.callback_query_handler(lambda call: call.data.startswith("newtask"))
def set_new_task_name(call):
    message = call.message
    trello_username = utils.get_trello_username_by_chat_id('chat.csv', message.from_user.id)
    trello = TrelloManager(trello_username)
    board_id = call.data.split("_")[1]
    keyboard = keyboards.get_list_btn(trello, board_id, 'list_name')
    bot.send_message(
        call.from_user.id,
        messages.SELECT_LIST,
        reply_markup=keyboard
    )
    bot.set_state(call.from_user.id, CreateNewTask.name, message.chat.id)
    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        data['task_board_id'] = board_id


@bot.callback_query_handler(lambda call: call.data.startswith('list_name'))
def set_list_id_for_new_task(call):
    message = call.message
    data_ = call.data.split("_")[2]
    msg = bot.send_message(call.from_user.id, messages.TASK_NAME)
    bot.set_state(call.from_user.id, CreateNewTask.name, message.chat.id)
    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        data['task_list_id'] = data_
    bot.register_next_step_handler(msg, set_task_name)


def set_task_name(message):
    msg = bot.send_message(message.from_user.id, messages.TASK_DECS)
    bot.set_state(message.from_user.id, CreateNewTask.description, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['task_name'] = message.text
        params = {
            'name': data.get('name'),
            'desc': data.get('desc')
        }
    bot.register_next_step_handler(msg, set_task_description)


def set_task_description(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['task_desc'] = message.text
        board_id = data['task_board_id']
    trello_username = utils.get_trello_username_by_chat_id('chat.csv', message.from_user.id)
    bot.send_message(message.from_user.id, 'Foydalanuvchilar yuklanmoqda...\nIltimos kutib turing.')
    keyboard = keyboards.get_members_btn(trello_username, board_id, 'new_task_member')
    bot.set_state(message.from_user.id, CreateNewTask.members, message.chat.id)
    bot.send_message(
        message.from_user.id,
        messages.TASK_MEMBERS, reply_markup=keyboard
    )


@bot.callback_query_handler(lambda c: c.data.startswith("new_task_member"))
def get_list_id_for_new_task(call):
    message = call.message
    list_id = call.data.split("_")[3]
    bot.set_state(call.from_user.id, CreateNewTask.name, message.chat.id)
    user_name = utils.get_trello_username_by_chat_id('chat.csv', call.from_user.id)
    trello = TrelloManager(user_name)

    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        data["member_id"] = list_id
        print(data)
        param = {
            'board': data.get('task_board_id'),
            'idList': data.get('task_list_id'),
            'name': data.get('task_name'),
            'description': data.get('task_desc'),
            'members': data.get('member_id')
        }
        trello.create_new_card(param)
    bot.send_message(call.from_user.id, 'Malumotlar saqlandi')


def my_commands():
    return [
        telebot.types.BotCommand('/start', 'Boshlash'),
        telebot.types.BotCommand('/register', "Ro'yxatdan o'tish"),
        telebot.types.BotCommand('/new', "Yangi task yaratish"),
        telebot.types.BotCommand('/boards', "Doskalarni ko'rish"),
        telebot.types.BotCommand('/cancel', 'Bekor qilish'),
        telebot.types.BotCommand('/help', 'Yordam')
    ]


if __name__ == "__main__":
    print('started...')
    bot.set_my_commands(my_commands())
    bot.infinity_polling()
