import csv
import os


def write_chat_csv(file_path, message):
    print('csv write is working')
    header = ['chat_id', 'first_name', 'last_name', 'trello_username']
    row = {
        'chat_id': message.from_user.id,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'trello_username': message.text
    }
    # print('row\n', row)
    with open(file_path, 'a', newline='\n') as file:
        csv_writer = csv.DictWriter(file, header)
        if os.path.getsize(file_path) == 0:
            csv_writer.writeheader()
        csv_writer.writerow(row)
    print('csv data saved successfully')


def check_chat_id_from_csv(file_path, chat_id):
    print('check is working')
    with open(file_path, encoding='utf8') as file:
        csv_reader = csv.DictReader(file)
        data = [int(data.get("chat_id")) for data in csv_reader]
        if chat_id in data:
            return True
        return False


def get_trello_username_by_chat_id(file_path, chat_id):
    with open(file_path, encoding='utf8') as file:
        print('get_user name is working')
        csv_reader = csv.DictReader(file)
        users = [
            data.get("trello_username")
            for data in csv_reader
            if int(data.get('chat_id')) == chat_id
        ]
        return users[0] if users else None


def get_members_task_messages(card_data, member_id):
    msg = ''
    for data in card_data:
        if member_id in data.get('idMembers'):
            msg += f"{data.get('idShort')} - <a href=\"{data.get('url')}\">{data.get('name')}</a>\n"
    return msg
