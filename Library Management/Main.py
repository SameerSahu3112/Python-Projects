from Connection import create_connection
try:
    from tabulate import tabulate
except ImportError:
    raise ImportError("The tabulate pacakge is required")

def menu():
    print("#### Welcome To Library ####")
    print("1. Admin")
    print("2. Student")
    print("3.Exit")
    

