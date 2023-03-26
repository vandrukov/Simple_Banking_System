import random

accounts = {}
IIN = "400000"


def acсount():
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
    check_sum = str(random.randint(0, 9))
    pin = str(random.randint(1000, 9999))
    while True:
        if str(IIN + account_number + check_sum) not in accounts:
            accounts[IIN + account_number + check_sum] = pin
            break
        else:
            card = random.randint(100000000, 999999999)
    print("Your card has been created")
    print("Your card number:")
    print(IIN + account_number + check_sum)
    print("Your card PIN:")
    print(pin)


def login_account():
    card = input("Enter your card number:")
    pin = input("Enter your PIN:")
    if (card, pin) in accounts.items():
        print("You have successfully logged in!")
        acсount()
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
