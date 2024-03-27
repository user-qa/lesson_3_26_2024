from sql_connect import  DATABASE


user_table = """
        CREATE TABLE user_table(
        user_id SERIAL,
        name VARCHAR(45) NOT NULL,
        phone_number CHAR(12) Primary Key
        )"""

card_table = """
        CREATE TABLE card_table (
        card_number CHAR(16) PRIMARY KEY,
        password CHAR(4) CHECK (password ~ '^[0-9]{4}$'),
        expire_date DATE NOT NULL,
        balance NUMERIC(38, 0) NOT NULL
        )"""

card_and_user = """
        CREATE TABLE card_user_table(
        id Serial Primary Key,
        phone_number CHAR(12) not null references user_table(phone_number),
        card_number char(16) not null references card_table(card_number)
        )"""

history = """
        Create table history(
        id Serial Primary Key,
        card_number char(16) not null references card_table(card_number),
        balance_change_history text not null
        )"""

blocked_cards = """
        CREATE TABLE blocked_cards(
        card_number char(16) primary key
        )"""
tables = [ user_table,card_table,card_and_user,history,blocked_cards ]

for i in tables:
    DATABASE.connect(i, 'create')


