def student_menu():
    student_choice = input("Already Registered (Y/N): ").upper()
    if student_choice == 'Y':
        print("Login")
        try:
            id_check = int(input("Enter Your Student ID: "))
            password_check = int(input("Enter Your Password: "))
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
            db.close()
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
        print("Your Student ID Is ",student_id)
        query = "INSERT INTO students (student_name, phone, Date_of_birth) VALUES(%s, %s, %s)"
        mycursor.execute(query, (student_name, phone, date_of_birth))
        db.commit()
        mycursor.execute("SELECT LAST_INSERT_ID()")
        student_id = mycursor.fetchone()[0]
    db.close()

def issue_books():
    print("Issue Books")
    try:
        book_id = int(input("Enter Book ID: "))
        student_id = int(input("Enter Your Student ID: "))
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
    mycursor.execute(query_insert, (book_id, student_id))
    mycursor.execute(query_update, (book_id,))
    db.commit()
    db.close()
    print("Book issued successfully.")

def return_books():
    print("Return Books")
    try:
        book_id = int(input("Enter Book ID: "))
        student_id = int(input("Enter Your Student ID: "))
    except ValueError:
        print("Invalid Input. Please Enter Numeric Values.")
        return
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query_check = "SELECT * FROM issued_books WHERE book_id = %s AND student_id = %s"
    mycursor.execute(query_check, (book_id, student_id))
    result = mycursor.fetchone()
    if result is None:
        print("No record found for this book and student.")
        return
    query_check_status = "SELECT status FROM issued_books WHERE book_id = %s AND student_id = %s"
    mycursor.execute(query_check_status, (book_id, student_id))
    status_result = mycursor.fetchone()
    if status_result is None or status_result[0].lower() == "returned":
        print("This book has already been returned.")
        return

    query_delete = "UPDATE issued_books SET status = 'returned' WHERE book_id = %s AND student_id = %s"
    query_update = "UPDATE books SET status = 'available' WHERE book_id = %s"
    mycursor.execute(query_delete, (book_id, student_id))
    mycursor.execute(query_update, (book_id,))
    db.commit()
    db.close()
    print("Book returned successfully.")

def profile():
    print("Profile")
    try:
        student_id = int(input("Enter Your Student ID: "))
    except ValueError:
        print("Invalid Input. Please Enter Numeric Values.")
        return
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT * FROM students WHERE student_id = %s"
    mycursor.execute(query, (student_id,))
    result = mycursor.fetchone()
    if result:
        print("Student ID:", result[0])
        print("Name:", result[1])
        print("Phone:", result[2])
        print("Date of Birth:", result[3])
    else:
        print("No student found with this ID.")
    history_query = "SELECT b.book_name, ib.status FROM issued_books ib JOIN books b ON ib.book_id = b.book_id WHERE ib.student_id = %s"
    mycursor.execute(history_query, (student_id,))
    history = mycursor.fetchall()
    if history:
        print("Borrowed Books:")
        for h in history:
            print("Book Name:", h[0], "| Status:", h[1])
    else:
        print("No borrowed books found.")   
    db.close()

def borrowed_books():
    print("Borrowed Books")
    try:
        student_id = int(input("Enter Your Student ID: "))
    except ValueError:
        print("Invalid Input. Please Enter Numeric Values.")
        return
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT b.book_name, ib.status FROM issued_books ib JOIN books b ON ib.book_id = b.book_id WHERE ib.student_id = %s AND ib.status = 'issued'"
    mycursor.execute(query, (student_id,))
    result = mycursor.fetchall()
    if result:
        for r in result:
            print("Book Name:", r[0], "| Status:", r[1])
    else:
        print("No Current Issued books found.")
    db.close()

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
