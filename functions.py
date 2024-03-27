from SQL_CONNECTIONS.sql_connect import DATABASE
from datetime import datetime


def is_blocked(card_number):
    blocked_numbers_query = 'select * from blocked_cards'
    blocked_numbers_data = DATABASE.connect(blocked_numbers_query, 'select')
    blocked_numbers_list = [i[0] for i in blocked_numbers_data]
    if card_number not in blocked_numbers_list:
        return False
    else:
        return True


def password_check(card_number):
    query_password = f"Select password from card_table where card_number = '{card_number}'"
    actual_password = DATABASE.connect(query_password, 'select')[0][0]
    n = 1
    while n <= 3:
        if n == 3:
            print(f'Be Careful, this is your last attempt!!!')
        password = input('Please enter the password: ')
        if password == actual_password:
            return True
        n += 1
    else:
        block_query = f"INSERT INTO blocked_cards (card_number) values('{card_number}')"
        DATABASE.connect(block_query, 'insert')
        print('Your card is blocked now! To unblock your card, you must visit our head office!')
        return 'blocked'


def expire_date_check(date):
    today_date = datetime.today().date()
    today = datetime.strptime(f'{today_date}', "%Y-%m-%d")
    expire_date = datetime.strptime(date, "%Y-%m-%d")

    if today < expire_date:
        return True
    elif today > expire_date:
        return False


def is_card_available(card_number):
    query_numbers = 'Select card_number from card_table'
    card_numbers_data = DATABASE.connect(query_numbers, 'select')
    card_numbers_list = [i[0] for i in card_numbers_data]
    if card_number in card_numbers_list:
        return True
    else:
        return False


def is_user_available(phone_number):
    query_phone = 'select phone_number from user_table'
    phone_data = DATABASE.connect(query_phone, 'select')
    phone_list = [i[0] for i in phone_data]
    if phone_number in phone_list:
        return True
    else:
        return False


def check_balance(card_number):
    query_balance = f"Select balance from card_table where card_number = '{card_number}'"
    balance = DATABASE.connect(query_balance, 'select')
    return f'Your balance: {balance[0][0]}'


def card_history(card_number):
    query_history = f"Select balance_change_history from history where card_number = '{card_number}'"
    history_data = DATABASE.connect(query_history, 'select')
    history_list = [i[0] for i in history_data]
    response = ''
    for i in history_list:
        response += '\n' + i


def format_phone_check():
    while True:
        phone_number = input('Enter a phone number: ')
        if phone_number.isdigit() and len(phone_number) == 12:
            if is_user_available(phone_number):
                print('User with this phone number is already signed up!')
            else:
                return phone_number
        else:
            print('Invalid phone number!')


def format_card_number_check():
    while True:
        card_number = input('Enter the card number: ')
        if card_number.isdigit() and len(card_number) == 16:
            return card_number
        else:
            print('Invalid card number!')


def format_password_check():
    while True:
        password = input('Enter the password: ')
        if password.isdigit() and len(password) == 4:
            return password
        else:
            print('Invalid password!')





def format_expire_date_check():
    date = input('Enter the expiry date: ')
    if date[:4].isdigit() == True and date[5:7].isdigit() == True and date[8:10].isdigit() == True:
        if 1<=int(date[5:7]) <= 12 and 1<= int(date[8:10]) <= 31:
            if expire_date_check(date) == True:
                return date
    return format_expire_date_check()


def transaction(card_number):
    print('Recipient card number...')
    recipient_card_number = format_card_number_check()
    if is_card_available(recipient_card_number) == True:
        recipient_name_query = f"select name from user_table ut inner join card_user_table cut on ut.phone_number = cut.phone_number inner join card_table ct on ct.card_number = cut.card_number where cut.card_number = '{recipient_card_number}'"
        recipient_name = DATABASE.connect(recipient_name_query, 'select')[0]
        cont = input(f'Is the recipient name {recipient_name}? Type y/n: ')
        if cont == 'y':
            amount = int(input('Enter the amount you wanna transfer: '))
            recipient_balance_query = f"select balance from card_table where card_number = '{recipient_card_number}'"
            recipient_balance = DATABASE.connect(recipient_balance_query, 'select')[0][0]
            recipient_balance_change = f"update card_table set balance = {recipient_balance + amount} where card_number = '{recipient_card_number}' "

            sender_balance_query = f"select balance from card_table where card_number = '{card_number}'"
            sender_balance = DATABASE.connect(sender_balance_query, 'select')[0][0]
            sender_balance_change = f"update card_table set balance = {sender_balance - amount} where card_number = '{card_number}' "

            DATABASE.connect(recipient_balance_change, 'update')
            DATABASE.connect(sender_balance_change, 'update')

            time_now = datetime.now()
            sender_history = f"{amount} dollars sent to {recipient_name} {recipient_card_number} at {time_now}"
            recipient_history = f"{amount} dollars received from {card_number} at {time_now} "

            # history_insert_sender = f"""insert into history (card_number, balance_change_history) values({card_number}, '{sender_history}')"""
            # history_insert_recipient = f"""insert into history (card_number, balance_change_history) values({recipient_card_number}, '{recipient_history}')"""
            # DATABASE.connect(history_insert_sender, 'insert')
            # DATABASE.connect(history_insert_recipient, 'insert')

            return 'Successfully Completed'
        else:
            return 'Operation Canceled'
    else:
        return 'Transactions Can Only Be Made Between Users Of My App'