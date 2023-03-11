# User
ALL_USERS = 'SELECT * FROM users'
GET_USER_BY_CHAT = 'SELECT * FROM users WHERE chat_id = %s'
REGISTER_USER = '''
    INSERT INTO 
    users(chat_id, username, trello_username, trello_id, firstname, lastname)
    VALUES (%s, %s, %s, %s, %s)
'''

UPDATE_USER_TRELLO_BY_CHAT_ID = '''
    UPDATE users
    SET trello_username = %s, trello_id = %s
    WHERE chat_id = %s
'''

GER_USER_BY_TRELLO_ID = '''
    SELECT trello_id from users WHERE trello_id = %s
'''

# Boards
UPSERT_BOARDS = '''
    INSERT INTO boards(name, trello_id) 
    VALUES (%s, %s)
    ON CONFLICT (trello_id)
    DO UPDATE SET name=excluded.name
'''

GET_BOARD_BY_TRELLO_ID = '''
    SELECT * FROM boards  WHERE  trello_id = %s
    
'''

# Board Users
UPSERT_BOARD_USERS = '''
    INSERT INTO boards_users(board_id, user_id)  VALUES (%s, %s)
    ON CONFLICT(board_id, user_id) DO NOTHING 
'''

GET_USER_BOARDS = '''
    SELECT B.name AS name, b.id as "board id"  FROM boards_users as bu
    INNER JOIN boards b ON bu.board_id = b.id
    WHERE bu.user_id = %s
'''

# List
UPSERT_LIST = '''
    INSERT INTO lists(name, trello_id, board_id) VALUES (%s, %s, %s)
    ON CONFLICT (trello_id) DO UPDATE SET name=excluded.name, board_id=excluded.board_id
'''

GET_LISTS_BY_TRELLO_ID = '''
    SELECT * FROM lists WHERE trello_id = %s
'''

# Cards 
UPSERT_CARDS = '''
    INSERT INTO cards(name, trello_id, url, description, list_id)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (trello_id)
    DO UPDATE SET name=excluded.name,
    url=excluded.url,
    description=excluded.description,
    list_id=excluded.list_id
'''

GET_CARD_ID_BY_TRELLO_ID = '''
    SELECT * FROM cards WHERE trello_id = %s
'''

# Cards members
GET_CARD_MEMBERS_BY_CARD_ID = '''
    SELECT * FROM cards_users WHERE card_id = %s
'''

INSERT_CARD_MEMBER = '''
   INSERT INTO cards_users(card_id, user_id) VALUES (%s, %s)
'''

DELETE_CARD_MEMBER = '''
    DELETE FROM cards_users WHERE card_id = %s AND user_id = %s
'''

GET_USER_CARDS_BY_BOARD_ID = '''
    SELECT * FROM cards_users AS cu
    INNER JOIN cards c ON c.id = cu.card_id
    INNER JOIN lists l ON c.list_id = l.id
    INNER JOIN boards b ON b.id = l.board_id
    WHERE b.id = %s AND cu.user_id = %s
'''