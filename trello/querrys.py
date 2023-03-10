# Users
ALL_USERS = "select * from users"
GET_USER_BY_CHAT_ID = "select * from users where chat_id = %s"
REGISTER_USER = """
    insert into
    users(chat_id, first_name, last_name, username)
    VALUES (%s, %s, %s, %s)
"""
UPDATE_USER_TRELLO_BY_CHAT_ID = """
    update users
    set trello_username = %s, trello_id = %s
    where chat_id = %s
"""
