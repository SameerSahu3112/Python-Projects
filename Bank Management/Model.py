class Customer:
    def __init__(self, customer_name, date_of_birth, email, phone, address, customer_password):
        from Connection_Bank import create_connection
        db = create_connection()
        mycursor = db.cursor()
        query = "INSERT into customer (customer_name, date_of_birth, email, phone, address, customer_password) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(query, (customer_name, date_of_birth, email, phone, address, customer_password))
        db.commit()
        db.close()

def get_info():
    print("##### SIGN IN #####")
    customer_name = input("Enter The Name: ")
    date_of_birth = input("Enter Your Date Of Birth (YYYY-MM-DD): ")
    email = input("Enter Your Email: ")
    phone = input("Enter Your Phone No.: ")
    if len(phone) != 10:
        print("Enter Valid Number")
    else:
        address = input("Enter Your Address: ")
        customer_password = input("Enter The Password: ")
        confirm_password = input("Confirm Your Password: ")
        if customer_password == confirm_password:
            print("Registration Complete")
            from Connection_Bank import create_connection
            db = create_connection()
            mycursor = db.cursor()
            query = "SELECT * FROM customer WHERE phone = %s"
            mycursor.execute(query, (phone,))
            result = mycursor.fetchall()
            print(result[0])
            login()
        else:
            print("Invalid Input")
        Customer(customer_name, date_of_birth, email, phone, address, customer_password)

def login():
    global customer_id
    print("##### LOGIN #####")
    try:
        customer_id = int(input("Enter Your ID: "))
        password = input("Enter Your Password: ")
    except ValueError:
        print("Enter Valid ID")
    from Connection_Bank import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT customer_id, customer_password FROM customer WHERE customer_id = %s AND customer_password = %s"
    mycursor.execute(query, (customer_id, password))
    result = mycursor.fetchall()
    for customer in result:
        customer_id_check = customer[0]
        customer_password_check = customer[1]
        if customer_id_check == customer_id and customer_password_check == password:
            print("Login Successfully")
            bank_customer_menu()
        else:
            print("Login ID OR Password Is Incorrect")

def bank_customer_menu():
    global customer_id
    from Connection_Bank import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT customer_name FROM customer WHERE customer_id = %s"
    mycursor.execute(query, (customer_id,))
    result = mycursor.fetchall()
    customer_name = result[0][0]
    while True:
        print(f"##### WELCOME {customer_name} #####")
        print("1. Account")
        print("2. Loan")
        print("3. Fixed Deposit")
        print("4. Reccuring Deposit")
        print("5. ATM")
        print("6. Exit")
        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Enter Valid Choice")

        if choice == 6:
            break


def customer_menu():
    while True:
        print("##### WELCOME TO MANIT BANK #####")
        print("1.Sign In")
        print("2.Login")
        print("3.Exit")
        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Enter Valid Choice")
        if choice == 1:
            get_info()
        elif choice == 2:
            login()
        elif choice == 3:
            break

customer_menu()





