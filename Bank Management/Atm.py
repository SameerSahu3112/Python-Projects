print("###### Welcome To ATM ######")
attempt = 3
pin = "1234"
from Connection_Bank import create_connection
db = create_connection()
mycursor = db.cursor()
query = "SELECT amount FROM customer WHERE customer_id = %s"
id_customer = int(input("Enter Your ID: "))
mycursor.execute(query, (id_customer))
balance = mycursor.fetchone()

def pin_check(pin,attempt):
    while True:
        user_pin = input("Please Enter Your 4-Digit PIN: ")
        if user_pin == pin:
            print("Access Granted!")
            break

        else:
            attempt -= 1
            print("Incorrect PIN. You Have ", attempt, "Attempts Left.")
            if attempt == 0:
                print("Your Account Has Been Locked. Please Contact Your Bank.")
                break

def menu():

    print("1.Check Balance")
    print("2.Withdraw Money")
    print("3.Deposit Money")
    print("4.Exit")

def check_balance():
    global balance
    print("Your Current Balance is $", balance)

def withdraw(amount):
    global balance
    if balance < amount:
        print("Insufficient Funds. Your Current Balance is $", balance)
    else:
        balance -= amount
        print("You Have Withdrawn $", amount)
        print("Your New Balance is $", balance)

def deposit(amount):
    global balance
    balance += amount
    print("You Have Deposited $", amount)
    print("Your New Balance is $", balance)

pin_check(pin, attempt)
while True:
    menu()
    choice = input("Please Select an Option: ")
    if choice == "1":
        check_balance()

    elif choice == "2":
        amount = float(input("Enter Amount To Withdraw: "))
        withdraw(amount)

    elif choice == "3":
        amount = float(input("Enter Amount To Deposit: "))
        deposit(amount)

    elif choice == "4":
        print("Thank You For Using Our ATM!")
        break
    
    else:
        print("Invalid Option. Please Try Again.")
