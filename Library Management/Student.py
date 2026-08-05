def student_menu():
    student_choice = input("Already Registered (Y/N): ").upper()
    if student_choice == 'Y':
        print("Login")
        try:
            id_check = input("Enter Your Student ID: ")
            password_check = input("Enter Your Password: ")
        except ValueError:
            print("Enter Valid ID")

        

        