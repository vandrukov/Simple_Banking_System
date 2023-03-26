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
###

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


def account():
    while True:
        print("""1. Balance
2. Log out
0. Exit""")
        action = input()
        if action == "1":
            print("Balance: 0")
        elif action == "2":
            print("You have successfully logged out!")
            break
        else:
            print("Bye!")
            quit()


def create_account():
    account_number = str(random.randint(100000000, 999999999))
    check = check_sum(lunh(IIN + account_number))
    pin = str(random.randint(1000, 9999))
    while True:
        if check_card_exist(str(IIN + account_number + str(check))):
        #if str(IIN + account_number + str(check)) not in accounts:
            insert_data(ID, str(IIN + account_number + str(check)), pin, 0)
            #accounts[IIN + account_number + str(check)] = pin
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
        account()
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
