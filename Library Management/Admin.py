def pin_check(pin="1234",attempt=3):
    while True:
        user_pin = input("Please Enter Your 4-Digit PIN: ")
        if user_pin == pin:
            print("Access Granted!")
            menu()
            break
        else:
            attempt -= 1
            print("Incorrect PIN. You Have ", attempt, "Attempts Left.")
            if attempt == 0:
                print("Try Again Later")
                break

def add_book():
    book_name = input("Enter The Name Of The Book: ").strip()
    author_name = input("Enter The Name Of The Author: ").strip()
    series_name = input("Enter The Name Of The Series: ").strip()

    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    if not book_name or not author_name or not series_name:
        print("All Fields Are Required!")
        return
    query = "SELECT * FROM books WHERE book_name = %s AND author_name = %s "
    mycursor.execute(query, (book_name, author_name))
    result = mycursor.fetchone()
    if result:
        print("Book Already Exists!")
        return
    books = "INSERT INTO books (book_name, author_name, series_name) VALUES(%s, %s, %s)"
    mycursor.execute(books, (book_name, author_name, series_name))
    print("Book Added Successfully!")
    mycursor.execute("SELECT LAST_INSERT_ID()")
    book_id = mycursor.fetchone()[0]
    print("Your Book ID Is ",book_id)
    db.commit()
    db.close()
    return 

def delete_book():
    book_id = input("Enter The ID of The Book You Want To Delete: ")
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    delete = "DELETE FROM books WHERE book_id = %s"
    mycursor.execute(delete, (book_id,))
    db.commit()
    print("Book Deleted Successfully!")

def book_status():
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    mycursor.execute("SELECT book_name, status FROM books")
    status = mycursor.fetchall()
    for book_name, book_status in status:
        print(book_name, ":", book_status)

def view_books():
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    author_name = input("Enter The Name Of The Author: ").strip()
    series_name = input("Enter The Name Of The Series: ").strip()
    book_name = input("Enter The Name Of The Book: ").strip()
    book_id = input("Enter The ID Of The Book: ").strip()
    conditions = []
    values = []
    if author_name:
        conditions.append("author_name LIKE %s")
        values.append(f"%{author_name}%")
    if series_name:
        conditions.append("series_name LIKE %s")
        values.append(f"%{series_name}%")
    if book_name:
        conditions.append("book_name LIKE %s")
        values.append(f"%{book_name}%")
    if book_id:
        conditions.append("book_id = %s")
        values.append(book_id)
    if conditions:
        view = "SELECT * FROM books WHERE " + " OR ".join(conditions)
        mycursor.execute(view, tuple(values))
        result = mycursor.fetchall()
        for r in result:
            print(r)
        if not result:
            print("No Books Found!")
    else:
        view = "SELECT * FROM books"
        mycursor.execute(view)
        result = mycursor.fetchall()
        for r in result:
            print(r)


def update_book():
    id_book = input("Enter The ID Of The Book: ").strip()
    series_name = input("Enter The Name Of The Series You Want To Update: ").strip()
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    if not id_book or not series_name:
        print("All Fields Are Required!")
        return 
    query = "UPDATE books SET series_name = %s WHERE book_id = %s"
    mycursor.execute(query, (series_name, id_book))
    db.commit()
    print("Book Updated Successfully!")

def menu():
    while True:
        print("#### Welcome To Library ####")
        print("1.Book Management")
        print("2.Student Management")
        print("3.Exit")
        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid Input")
            continue
        if choice == 1:
            book_management()
        elif choice == 2:
            student_management()
        else:
            print("Exiting.....")
            break
            
def book_management():
    while True:
        print("#### Book Management ####")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. View Books")
        print("4. Update Book")
        print("5. Book Status")
        print("6. Book History")
        print("7. Exit")
        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid Input")
            continue
        if choice == 1:
            add_book()
        elif choice == 2:
            delete_book()
        elif choice == 3:
            view_books()
        elif choice == 4:
            update_book()
        elif choice == 5:
            book_status()
        elif choice == 6:
            book_history()
        elif choice == 7:
            break
        else:
            print("Invalid Input")

def view_students():
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    student_id = input("Enter The ID Of The Student: ").strip()
    if not student_id:
        mycursor.execute("SELECT * FROM students")
    else:                            
        mycursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        result = mycursor.fetchall()
        for r in result:    
            print(r) 

def delete_student():
    try:
        student_id = int(input("Enter The ID Of The Student You Want To Delete: ").strip())
    except ValueError:
        print("Invalid Input. Please Enter Numeric Values.")
    if not student_id:
        choice = print("Do You Want To Delete The Student? (Y/N): ")
        if choice.lower() == 'y':
            delete_student()
        else:
            print("Student Deletion Cancelled.")
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    delete = "DELETE FROM students WHERE student_id = %s"
    mycursor.execute(delete, (student_id,))
    print("Student Deleted Successfully!")
    db.commit()

def student_management():
    while True:
        print("#### Student Management ####")
        print("1. View Students")
        print("2. Delete Student")
        print("3. Active Students")
        print("4. Student History")
        print("5. Exit")
        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid Input")
            continue
        if choice == 1:
            view_students()
        elif choice == 2:
            delete_student()
        elif choice == 3:
            active_student()
        elif choice == 4:
            student_history()
        elif choice == 5:
            break
        else:
            print("Invalid Input")

def book_history():
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    book_id = input("Enter The ID Of The Book: ").strip()
    if not book_id:
        print("Book ID is required!")
        return
    query = """
        SELECT b.book_name, COUNT(*) AS issue_count
        FROM issued_books ib
        JOIN books b ON ib.book_id = b.book_id
        WHERE ib.book_id = %s
        GROUP BY b.book_name
    """
    mycursor.execute(query, (book_id,))
    result = mycursor.fetchone()
    if result:
        print(result[0], "has been issued", result[1], "times.")
    else:
        print("No history found for this book.")


def active_student():
    try:
        student_id = int(input("Enter The ID Of The Student: "))
    except ValueError:
        print("Invalid Input")
        return 
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT book_id FROM issue_books WHERE student_id = %s AND status = 'issued' "
    mycursor.execute(query, (student_id,))
    books = mycursor.fetchall()
    for book in books:
        print(book[0])
    query_name = "SELECT book_name FROM books WHERE book_id = %s"
    mycursor.execute(query_name, (student_id,))
    name = mycursor.fetchall()
    for names in name:
        print(names[0])

def student_history():
    try:
        student_id = int(input("Enter The ID Of The Student: "))
    except ValueError:
        print("Invalid Input")
        return 
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    query = "SELECT * FROM students WHERE student_id = %s"
    mycursor.execute(query, (student_id,))
    result = mycursor.fetchone()
    query_history = "SELECT b.book_name, ib.status FROM issued_books ib JOIN books b ON ib.book_id = b.book_id WHERE ib.student_id = %s"
    mycursor.execute(query_history, (student_id,))
    history = mycursor.fetchall()
    if history:             
        print("Borrowed Books:")
        for h in history:
            print("Book Name:", h[0], "| Status:", h[1])
    else:
        print("No borrowed books found.")
    if result:
        print("Student ID:", result[0])
        print("Name:", result[1])
        print("Phone:", result[2])
        print("Date of Birth:", result[3])
    else:
        print("No student found with this ID.")
