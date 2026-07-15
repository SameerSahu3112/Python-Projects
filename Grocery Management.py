def customer():
    print("Welcome Customer!")
    print("1. View Grocery Items")
    print("2. Buy Items")
    print("3. View Cart")
    print("4. Update Cart")
    print("5.Generate Bill")
    print("6.Back To Main Menu")

def admin():
    print("Welcome Owner!")
    print("1. Add Grocery items")
    print("2. Update Grocery items")
    print("3. Delete Grocery items")
    print("4. View Grocery items")
    print("5. Change Price of Grocery items")
    print("6. Back To Main Menu")
    
def main_menu(user_pin=1234,attempt=3):
    print("###### Grocery Management System ######")
    print(" 1. Customer ")
    print(" 2. Owner ")
    choice = input("Enter Your Choice: ")
    if choice == '1':
        customer()
    elif choice == '2':
        while True:
            user_pin = input("Please Enter Your 4-Digit PIN: ")
            if user_pin == "1234":  # Replace "1234" with the actual PIN
                admin()
                break
            else:
                attempt -= 1
                print("Incorrect PIN, You Have ", attempt, "Attempts Left.")
                if attempt == 0:
                    print("Your Account Has Been Locked. Please Try Again Later.")
                    break
    else:
        print("Invalid Choice! Try Again.")
        main_menu(user_pin, attempt)
 


