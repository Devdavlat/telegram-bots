from psycopg2.extras import RealDictCursor
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from db import connection, queries


# def get_inline_boards_btn(user_id, action):
#     inline_boards_btn = InlineKeyboardMarkup()


