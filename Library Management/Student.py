def student_menu(attempts=3):
    student_choice = input("Already Registered (Y/N): ").upper()
    if student_choice == 'Y':
        print("Login")
        try:
            id_check = int(input("Enter Your Student ID: "))
            password_check = int(input("Enter Your Password: "))
            if not id_check or not password_check:
                print("Forgot Password? Your Password Is Your Date Of Birth (DD-MM-YYYY)")
        except ValueError:
            print("Enter Valid ID")
        from Connection import create_connection
        db = create_connection()
        mycursor = db.cursor()
        query = "SELECT * FROM students WHERE student_id = %s AND dob = %s"
        mycursor.execute(query, (id_check, password_check))
        result = mycursor.fetchone()
        if result:
            print("Login Successful!")
            menu()
        else:
            print("Invalid ID or Password!")
            print("Password Is Your Date Of Birth (DD-MM-YYYY)")
            attempts -= 1
            if attempts > 0:
                print(f"You have {attempts} attempts left.")
                student_menu(attempts)
                student_menu(attempts=3)

    else:
        print("Register")
        try:
            student_name = input("Enter Your Name: ")
            phone = int(input("Enter Phone Number: "))
            if len(str(phone)) != 10:
                print("Enter Valid Phone Number")
                return
            if not student_name or not phone:
                print("Enter Valid Information")
                return
            date_of_birth = int(input("Enter Your Date Of Birth (DD-MM-YYYY): "))
        except ValueError:
            print("Enter Valid Information")
        print("Registration Successful!")
        print("Your Password Is Your Date Of Birth")
        from Connection import create_connection
        db = create_connection()
        mycursor = db.cursor()
        query = "INSERT INTO students (name_student, phone, dob) VALUES(%s, %s, %s)"
        mycursor.execute(query, (student_name, phone, date_of_birth))
        db.commit()
        mycursor.execute("SELECT LAST_INSERT_ID()")
        student_id = mycursor.fetchone()[0]
        print("Your Student ID Is ",student_id)
        db.close()
        menu()
        return 

def issue_books(id_check):
    print("Issue Books")
    try:
        book_id = int(input("Enter Book ID: "))
    except ValueError:
        print("Invalid Input. Please Enter Numeric Values.")
        return
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT status FROM books WHERE book_id = %s"
    mycursor.execute(query, (book_id,))
    result = mycursor.fetchone()
    if result is None:
        print("Book does not exist.")
        return
    if result[0].lower() == "issued":
        print("Book is already issued.")
        return
    query_insert = "INSERT INTO issued_books (book_id, student_id) VALUES(%s, %s)"
    query_update = "UPDATE books SET status = 'issued' WHERE book_id = %s"
    mycursor.execute(query_insert, (book_id, id_check))
    mycursor.execute(query_update, (book_id,))
    db.commit()
    print("Book issued successfully.")

def return_books(id_check):
    print("Return Books")
    try:
        book_id = int(input("Enter Book ID: "))
    except ValueError:
        print("Invalid Input. Please Enter Numeric Values.")
        return
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query_check = "SELECT * FROM issued_books WHERE book_id = %s AND student_id = %s"
    mycursor.execute(query_check, (book_id, id_check))
    result = mycursor.fetchone()
    if result is None:
        print("No record found for this book and student.")
        return
    query_check_status = "SELECT status FROM issued_books WHERE book_id = %s AND student_id = %s"
    mycursor.execute(query_check_status, (book_id, id_check))
    status_result = mycursor.fetchone()
    if status_result is None or status_result[0].lower() == "returned":
        print("This book has already been returned.")
        return

    query_delete = "UPDATE issued_books SET status = 'returned' WHERE book_id = %s AND student_id = %s"
    query_update = "UPDATE books SET status = 'available' WHERE book_id = %s"
    mycursor.execute(query_delete, (book_id, id_check))
    mycursor.execute(query_update, (book_id,))
    db.commit()
    print("Book returned successfully.")

def profile(id_check):
    print("Profile")
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT * FROM students WHERE student_id = %s"
    mycursor.execute(query, (id_check,))
    result = mycursor.fetchone()
    if result:
        print("Student ID:", result[0])
        print("Name:", result[1])
        print("Phone:", result[2])
        print("Date of Birth:", result[3])
    else:
        print("No student found with this ID.")
    history_query = "SELECT b.book_name, ib.status FROM issued_books ib JOIN books b ON ib.book_id = b.book_id WHERE ib.student_id = %s"
    mycursor.execute(history_query, (id_check,))
    history = mycursor.fetchall()
    if history:
        print("Borrowed Books:")
        for h in history:
            print("Book Name:", h[0], "| Status:", h[1])
    else:
        print("No borrowed books found.")   

def borrowed_books(id_check):
    print("Borrowed Books")
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT b.book_name, ib.status FROM issued_books ib JOIN books b ON ib.book_id = b.book_id WHERE ib.student_id = %s AND ib.status = 'issued'"
    mycursor.execute(query, (id_check,))
    result = mycursor.fetchall()
    if result:
        for r in result:
            print("Book Name:", r[0], "| Status:", r[1])
    else:
        print("No Current Issued books found.")

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
        if choice == 1:
            issue_books()           
        elif choice == 2:   
            return_books()
        elif choice == 3:
            from Admin import view_books
            view_books()
        elif choice == 4:
            profile()
        elif choice == 5:
            borrowed_books()
        elif choice == 6:
            print("Exiting.....")
            break   
