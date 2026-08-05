def student_menu():
    student_choice = input("Already Registered (Y/N): ").upper()
    if student_choice == 'Y':
        print("Login")
        try:
            id_check = input("Enter Your Student ID: ")
            password_check = input("Enter Your Password: ")
        except ValueError:
            print("Enter Valid ID")
            from Connection import create_connection
            db = create_connection()
            mycursor = db.cursor()
            query = "SELECT * FROM students WHERE student_id = %s AND Date_of_birth = %s"
            mycursor.execute(query, (id_check, password_check))
            result = mycursor.fetchone()
            if result:
                print("Login Successful!")
                menu()
            else:
                print("Invalid ID or Password!")
                print("Password Is Your Date Of Birth (DD-MM-YYYY)")

    else:
        print("Register")
        try:
            student_name = input("Enter Your Name: ")
            phone = input("Enter Phone Number: ")
            date_of_birth = input("Enter Your Date Of Birth (DD-MM-YYYY): ")
        except ValueError:
            print("Enter Valid Information")
        print("Registration Successful!")
        print("Your Password Is Your Date Of Birth")
        query = "INSERT INTO students (student_name, phone, Date_of_birth) VALUES(%s, %s, %s)"
        mycursor.execute(query, (student_name, phone, date_of_birth))
        db.commit()

def menu():
    while True:
        print("#### Welcome To Library ####")
        print("1. Issue Books")
        print("2. Return Books")
        print("3. View Books")
        print("4. Profile")
        print("5. Borrowed Books")
        print("6. Exit")
        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid Input. Please Enter A Valid Option.")
            continue

