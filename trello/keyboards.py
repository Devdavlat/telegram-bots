from telebot.types import (
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton
)

from trello import TrelloManager


def get_get_boards_btn(trello_username):
    boards_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    boards = TrelloManager(trello_username).get_board()
    last_board = None
    second_last_board = None

    if len(boards) % 3 == 1:
        last_board = boards.pop()
    elif len(boards) % 3 == 2:
        last_board = boards.pop()
        second_last_board = boards.pop()

    for board_index in range(0, len(boards) - 1, 3):
        boards_btn.add(
            (boards[board_index].get('name')),
            KeyboardButton(boards[board_index + 1].get('name')),
            KeyboardButton(boards[board_index + 1].get('name'))
        )
    if last_board:
        boards_btn.add(KeyboardButton(last_board.get('name')))
        if second_last_board:
            boards_btn.add(KeyboardButton(second_last_board.get('name')))

    return boards_btn


def get_inline_boards_btn(trello_username, action):
    # print('get inline boards btn is working')
    inline_boards_btn = InlineKeyboardMarkup()
    boards = TrelloManager(trello_username).get_board()
    # print('len', len(boards))
    if len(boards) % 2 == 0:
        last_board = None
    else:
        last_board = boards.pop()
    for board_index in range(0, len(boards) - 1, 2):
        # print('board name', boards[board_index].get('name'))
        # print('board name 1 ', boards[board_index + 1].get('name'))
        inline_boards_btn.add(
            InlineKeyboardButton(boards[board_index].get('name'),
                                 callback_data=f'{action}_{boards[board_index].get("id")}'),
            InlineKeyboardButton(boards[board_index + 1].get('name'),
                                 callback_data=f'{action}_{boards[board_index + 1].get("id")}')
        )
    if last_board:
        inline_boards_btn.add(
            InlineKeyboardButton(last_board.get('name'),
                                 callback_data=f"{action}_{last_board.get('id')}")
        )

    return inline_boards_btn


def get_list_btn(trello, board_id, action):
    list_btn = InlineKeyboardMarkup()
    lists = trello.get_list_on_a_board(board_id)

    if len(lists) % 2 == 0:
        last_list = None
    else:
        last_list = lists.pop()
    print('name', lists[0].get('name'))

    for list_index in range(0, len(lists) - 1, 2):
        list_btn.add(
            InlineKeyboardButton(lists[list_index].get('name'),
                                 callback_data=f'{action}_{lists[list_index].get("id")}'),
            InlineKeyboardButton(lists[list_index + 1].get('name'),
                                 callback_data=f'{action}_{lists[list_index + 1].get("id")}')
        )
        if last_list:
            list_btn.add(
                InlineKeyboardButton(last_list.get('name'),
                                     callback_data=f'{action}_{last_list.get("id")}')
            )

    return list_btn


def get_inline_list_btn(trello, board_id, action):
    print('get inline keyboards is working')
    list_inline_btn = InlineKeyboardMarkup()
    lists = trello.get_list_on_a_board(board_id)
    # print(len(lists))
    if len(lists) % 2 == 1:
        last_board = lists.pop()
    else:
        last_board = None
    for list_index in range(0, len(lists) - 1, 2):
        list_inline_btn.add(
            InlineKeyboardButton(lists[list_index].get('name'),
                                 callback_data=f'{action}_{lists[list_index].get("id")}'),
            InlineKeyboardButton(lists[list_index + 1].get('name'),
                                 callback_data=f'{action}_{lists[list_index + 1].get("id")}')
        )
    if last_board:
        list_inline_btn.add(
            InlineKeyboardButton(last_board.get('name'),
                                 callback_data=f"{action}_{last_board.get('id')}")
        )

    return list_inline_btn


def get_members_btn(trello_username, board_id, action):
    members = TrelloManager(trello_username).get_board_members(board_id)
    members_btn = InlineKeyboardMarkup()
    last_member = None
    if len(members) % 2 == 1:
        last_member = members.pop()
    for member_index in range(0, len(members) - 1, 2):
        members_btn.add(
            InlineKeyboardButton(
                members[member_index].get('fullName'),
                callback_data=f"{action}_{members[member_index].get('id')}"
            ),
            InlineKeyboardButton(
                members[member_index + 1].get('fullName'),
                callback_data=f"{action}_{members[member_index + 1].get('id')}"
            )
        )
    if last_member:
        members_btn.add(
            InlineKeyboardButton(last_member.get('fullName'),
                                 callback_data=f"{action}_{last_member.get('id')}")
        )
    return members_btn
