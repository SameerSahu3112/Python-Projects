def pin_check(pin=1234,attempt=3):
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
    db.commit()
    print("Book Added Successfully!")

def delete_book():
    book_id = input("Enter The ID of The Book You Want To Delete: ")
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    delete = "DELETE FROM books WHERE book_id = %s"
    mycursor.execute(delete, (book_id))
    db.commit()
    print("Book Deleted Successfully!")

def book_status():
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    mycursor.execute("SELECT status FROM books")
    status = mycursor.fetchall()
    for s in status:
        print(s[0])

def view_books():
    from Connection import create_connection
    db = create_connection()
    mycursor = db.cursor()
    author_name = input("Enter The Name Of The Author: ").strip()
    if not author_name:
        series_name = input("Enter The Name Of The Series: ").strip()
        if not series_name:
            book_name = input("Enter The Name Of The Book: ").strip()
    view = "SELECT * FROM books WHERE author_name = %s OR series_name = %s OR book_name = %s"
    mycursor.execute(view, (author_name,series_name,book_name))
    result = mycursor.fetchall()
    for r in result:
        print(r)
    if not result:
        print("No Books Found!")
    if not book_name and not series_name and not author_name:
        view_books = "SELECT * FROM books"
        mycursor.execute(view_books)
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
            print("It Is Not Implemented Yet")
        elif choice == 7:
            break
        else:
            print("Invalid Input")