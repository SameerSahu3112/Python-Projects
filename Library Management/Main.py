from Connection import create_connection
try:
    from tabulate import tabulate
except ImportError:
    raise ImportError("The tabulate pacakge is required")

def menu():
    while True:
            print("#### Welcome To Library ####")
            print("1. Admin")
            print("2. Student")
            print("3. Exit")
            try:
                choice = int(input("Enter Your Choice: "))
            except ValueError:
                print("Invalid Input. Please Enter A Valid Option.")
                continue
            if choice == 1:
                from Admin import pin_check
                pin_check()
                break
            elif choice == 2:
                from Student import student_menu
                student_menu()
                break
            elif choice == 3:
                print("Exiting...")
                break
            else:
                print("Invalid Input. Please Enter A Valid Option.")



