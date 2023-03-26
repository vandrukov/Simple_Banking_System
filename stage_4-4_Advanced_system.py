import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

ID = 0
cur.execute("DROP TABLE IF EXISTS card;")
conn.commit()
cur.execute("""
    CREATE TABLE IF NOT EXISTS card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);
""")
conn.commit()


def insert_data(id, number, pin, balance):
    global ID
    cur.execute("INSERT INTO card(id, number, pin, balance) VALUES(?, ?, ?, ?)", (id, number, pin, balance))
    conn.commit()
    ID += 1


def check_card_exist(card_number):
    cur.execute('''
          SELECT *
          FROM card
          WHERE number = {};
          '''.format(card_number))
    dbrows = cur.fetchall()
    if not dbrows:
        return True
    else:
        return False


def check_card_pin(card_number, pin):
    cur.execute('''
          SELECT *
          FROM card
          WHERE number = {} AND pin = {};
          '''.format(card_number, pin))
    dbrows = cur.fetchall()
    if not dbrows:
        return False
    else:
        return True


IIN = "400000"


def lunh(num):
    a = 0
    for i in range(len(num)):
        if i % 2 == 0:
            b = int(num[i]) * 2
            if b >= 10:
                a += (b - 9)
            else:
                a += b
        else:
            a += int(num[i])
    return a


def check_sum(a):
    b = 0
    for i in range(0, 10):
        if (a + b) % 10 == 0:
            break
        else:
            b += 1
    return b


def balance(card):
    cur.execute('''
          SELECT balance
          FROM card
          WHERE number = {};
          '''.format(card))
    return cur.fetchall()[0][0]


def add_income(card):
    income = int(input("Enter income:"))
    cur.execute("UPDATE card SET balance = balance + {} WHERE number = {}".format(income, card))
    conn.commit()
    print("Income was added!")


def transfer(card):
    transfer_card = input("Enter card number:")
    if card == transfer_card:
        print("You can't transfer money to the same account!")
        return
    elif check_sum(lunh(transfer_card[:-1])) != int(transfer_card[-1]):
        print("Probably you made a mistake in the card number. Please try again!")
        return
    else:
        if check_card_exist(transfer_card):
            print("Such a card does not exist.")
        else:
            money = int(input("Enter how much money you want to transfer:"))
            print(money)
            print(balance(card))
            if money > balance(card):
                print("Not enough money!")
            else:
                cur.execute("UPDATE card SET balance = balance - {} WHERE number = {}".format(money, card))
                cur.execute("UPDATE card SET balance = balance + {} WHERE number = {}".format(money, transfer_card))
                conn.commit()
                print("Success!")


def close_account(card):
    cur.execute("DELETE FROM card WHERE number = {}".format(card))
    conn.commit()
    print("The account has been closed!")


def account(card):
    while True:
        print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
        action = input()
        if action == "1":
            print(balance(card))
        elif action == "2":
            add_income(card)
        elif action == "3":
            transfer(card)
        elif action == "4":
            close_account(card)
        elif action == "5":
            print("You have successfully logged out!")
            break
        elif action == "0":
            print("Bye!")
            quit()


def create_account():
    account_number = str(random.randint(100000000, 999999999))
    check = check_sum(lunh(IIN + account_number))
    pin = str(random.randint(1000, 9999))
    while True:
        if check_card_exist(str(IIN + account_number + str(check))):
            insert_data(ID, str(IIN + account_number + str(check)), pin, 0)
            break
        else:
            card = random.randint(100000000, 999999999)
            check = check_sum(lunh(IIN + card))
    print("Your card has been created")
    print("Your card number:")
    print(IIN + account_number + str(check))
    print("Your card PIN:")
    print(pin)


def login_account():
    card = input("Enter your card number:")
    pin = input("Enter your PIN:")
    if check_card_pin(card, pin):
        print("You have successfully logged in!")
        account(card)
    else:
        print("Wrong card number or PIN!")


def menu():
    while True:
        print("""1. Create an account
    2. Log into account
    0. Exit""")
        action = input()
        if action == "1":
            create_account()
        elif action == "2":
            login_account()
        else:
            print("Bye!")
            break


menu()
