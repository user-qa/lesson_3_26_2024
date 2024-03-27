from collections import namedtuple
from SQL_CONNECTIONS.sql_connect import DATABASE
import functions

User = namedtuple('User', ['phone_number', 'name', 'password', 'expire_date', 'balance', 'card_number'])


def process_login(phone_number):
    if functions.is_user_available(phone_number):
        card_number = input('Card number: ')
        if not functions.is_blocked(card_number):
            if functions.is_card_available(card_number):
                if functions.password_check(card_number):
                    return card_number
                else:
                    return 'blocked'
            else:
                process_login(phone_number)
                return False
        else:
            print('Your card is blocked! To unblock your card, you must visit our head office!')
            return 'blocked'
    else:
        return False


def register():
    print('Now you are going to sign up!')
    card_number = functions.format_card_number_check()
    while functions.is_card_available(card_number):
        print('This card is available')
        card_number = functions.format_card_number_check()

    phone_number = functions.format_phone_check()
    name = input('Enter your name: ')
    password = functions.format_password_check()
    expire_date = functions.format_expire_date_check()
    balance = int(input('Enter the balance: '))

    user = User(phone_number, name, password, expire_date, balance, card_number)

    query_user_insert = f"INSERT INTO user_table (name, phone_number) VALUES ('{user.name}', '{user.phone_number}')"
    query_card_insert = f"INSERT INTO card_table (card_number, password, expire_date, balance) VALUES ('{user.card_number}', '{user.password}', '{user.expire_date}', '{user.balance}')"
    query_card_and_user_insert = f"INSERT INTO card_user_table (phone_number, card_number) VALUES ('{user.phone_number}', '{user.card_number}')"

    insertions = [query_user_insert, query_card_insert, query_card_and_user_insert]
    for query in insertions:
        DATABASE.connect(query, 'insert')

    print('Successfully Signed Up')


while True:
    choice = input("""
            1. Login
            2. Register
            3. Exit
            Enter your choice: """)

    if choice == '1':
        phone_number = input('Enter your phone number: ')
        login_result = process_login(phone_number)

        if login_result == False:
            register()
        elif login_result == 'blocked':
            print('Your card is blocked!')
        else:
            print('Login successful!')
            card_number = login_result
            while True:
                operation = input("""
                    1. Balance
                    2. Transaction
                    3. Card History
                    4. Chiqish
                    """)
                if operation == '1':
                    print(functions.check_balance(card_number))
                elif operation == '2':
                    print(functions.transaction(card_number))
                elif operation == '3':
                    pass
                elif operation == '4':
                    break

    elif choice == '2':
        register()
    elif choice == '3':
        print('Thank you for using our service. Goodbye!')
        break
    else:
        print('Invalid choice. Please enter a valid option.')
