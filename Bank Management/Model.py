class Customer:
    def __init__(self, customer_name, date_of_birth, email, phone, address):
        from Connection_Bank import create_connection
        db = create_connection()
        mycursor = db.cursor()
        query = "INSERT into customer (customer_name, date_of_birth, email, phone, address) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(query, (customer_name, date_of_birth, email, phone, address))
        db.commit()
        db.close()

def get_info():
    customer_name = input("Enter The Name: ")
    date_of_birth = input("Enter Your Date Of Birth (YYYY-MM-DD): ")
    email = input("Enter Your Email: ")
    phone = input("Enter Your Phone No.: ")
    if len(phone) != 10:
        print("Enter Valid Number")
    address = input("Enter Your Address: ")
    customer_info = Customer(customer_name, date_of_birth, email, phone, address)

    






