cart = []
def customer():
    print("Welcome Customer!")
    print("1. View Grocery Items")
    print("2. Buy Items")
    print("3. View Cart")
    print("4. Update Cart")
    print("5.Generate Bill")
    print("6.Back To Main Menu")
    print("7.Search Product")
    while True:
        customer_choice = int(input("Enter Your Customer Choice: "))
        if customer_choice == 1:
            view_grocery_items()
        elif customer_choice == 6:
            break
        elif customer_choice == 7:
            search_grocery()


def admin():
    print("Welcome Owner!")
    print("1. Add Grocery items")
    print("2. Update Grocery items")
    print("3. Delete Grocery items")
    print("4. View Grocery items")
    print("5. Change Price of Grocery items")
    print("6. Back To Main Menu")
    print("7. Search Product")
    while True:
        admin_choice = int(input("Enter You Owner Choice: "))
        if admin_choice == 2:
            update_products_a()
        elif admin_choice == 4:
            view_grocery_items()
        elif admin_choice == 1:
            add_grocery_a()
        elif admin_choice == 6:
            break
        elif admin_choice == 7:
            search_grocery()
    
def main_menu(user_pin=1234,attempt=3):
    while True:
        print("###### Grocery Management System ######")
        print(" 1. Customer ")
        print(" 2. Owner ")
        print(" 3. Exit ")
        choice = input("Enter Your Choice: ")
        if choice == '1':
            customer()
        elif choice == '2':
            while True:
                user_pin = input("Please Enter Your 4-Digit PIN: ")
                if user_pin == "1234":  # Replace "1234" with the actual PIN
                    admin()
                    break
                else:
                    attempt -= 1
                    print("Incorrect PIN, You Have ", attempt, "Attempts Left.")
                    if attempt == 0:
                        print("Your Account Has Been Locked. Please Try Again Later.")
                        break
        elif choice == '3':
            break
        else:
            print("Invalid Choice! Try Again.")
            main_menu(user_pin, attempt)
 
def view_grocery_items():
    print("Grocery Items Available")
    print("1.Grains & Flours")
    print("2.Pulses")
    print("3.Spices")
    print("4.Cooking Essentials")
    print("5.Dairy Products")
    print("6.Beverages")
    print("7.Exit")
    print("You Will See Item In Order Of Product ID, Product Name, Price, Stock")
    
    while True:
        choice_grocery = int(input("Enter Your Choice No. For Viewing Grocery: "))

        if choice_grocery == 1:
           for product in products_Grains_Flour:
               print(product)

        elif choice_grocery == 2:
            for product in products_pulses:
                print(product)

        elif choice_grocery == 3:
            for product in product_spices:
                print(product)
        
        elif choice_grocery == 4:
           for product in product_cooking_essential:
               print(product)

        elif choice_grocery == 5:
            for product in product_dairy:
                print(product)

        elif choice_grocery == 6:
            for product in product_beverages:
                print(product)
        elif choice_grocery == 7:
            break

        else:
            print("Wrong Input")

# [Product ID, Product Name, Price, Stock]

products_Grains_Flour = [
    [101, "Rice", 60, 25],
    [102, "Wheat Flour", 30, 25],
    [103, "Maida", 40, 25],
    [104, "Sooji", 40, 25],
    [105, "Besan", 40, 25],
    [106, "Poha", 40, 25],
]
products_pulses = [
    [201, "Toor Dal", 50, 35],
    [202, "Moong Dal", 50, 35],
    [203, "Udad Dal", 50, 35],
    [204, "Chana Dal", 50, 35],
    [205, "Masoor Dal", 50, 35],
    [206, "Kabuli Chana", 50, 35],
    [207, "Rajma", 50, 35],
]
product_spices = [
    [301, "Elaichi", 20, 10],
    [302, "Dal Chini", 20, 10],
    [303, "Kali Mirch", 20, 10],
    [304, "Jeera", 20, 10],
    [305, "Dhaniya", 20, 10],
    [306, "Turmeric", 20, 10],
    [307, "Lal Mirch", 20, 10],
    [308, "Garam Masala", 20, 10],
    [309, "Saunf", 20, 10],
]
product_cooking_essential = [
    [401, "Cooking Oil", 100, 35],
    [402, "Ghee", 500, 25],
    [403, "Salt", 20, 35],
    [404, "Sugar", 20, 35],
    [405, "Vinegar", 40, 35],
    [406, "Soya Sauce", 40, 35],
]
product_dairy = [
    [501, "Milk", 60, 50],
    [502, "Cheese", 50, 50],
    [503, "Butter", 70, 50],
    [504, "Yogurt", 30, 50],
    [505, "Curd", 25, 50],
    [506, "Paneer", 100, 50],
]
product_beverages = [
    [601, "Tea", 10, 25],
    [602, "Coffee", 15, 25],
    [603, "Juice", 15, 25],
    [604, "Water", 10, 25],
    [605, "Energy Drink", 50, 25],
]

def update_products_a():
    print("1.Grains & Flours")
    print("2.Pulses")
    print("3.Spices")
    print("4.Cooking Essentials")
    print("5.Dairy Products")
    print("6.Beverages")
    Grocery_type = int(input("Enter The Grocery Choice: "))
    id = int(input("Enter The Product ID: "))
    quantity = int(input("Enter The New Quantity Of Stock: "))
    if Grocery_type == 1:
        for product in products_Grains_Flour:
            if product[0] == id:
                product[3] += quantity 

    elif Grocery_type == 2:
        for product in products_pulses:
            if product[0] == id:
                product[3] += quantity 
  
    elif Grocery_type == 3:
        for product in product_spices:
            if product[0] == id:
                product[3] += quantity 
  
    elif Grocery_type == 4:
        for product in product_cooking_essential:
            if product[0] == id:
                product[3] += quantity 
 
    elif Grocery_type == 5:
        for product in product_dairy:
            if product[0] == id:
                product[3] += quantity 
 
    elif Grocery_type == 6:
        for product in product_beverages:
            if product[0] == id:
                product[3] += quantity 
 
    else:
        print("Invalid Choice")

def add_grocery_a():
    print("1.Grains & Flours")
    print("2.Pulses")
    print("3.Spices")
    print("4.Cooking Essentials")
    print("5.Dairy Products")
    print("6.Beverages")
    Grocery_type = int(input("Enter The Grocery Choice: "))
    New_ID = int(input("Enter The New ID: "))
    New_Name = input("Enter The Name Of New Item: ")
    Price = int(input("Enter The Price Of New Item: "))
    Stock = int(input("Enter The Amount Of The New Item In The Stock: "))
    if Grocery_type == 1:
        products_Grains_Flour.append ([New_ID, New_Name, Price, Stock])
    elif Grocery_type == 2:
        products_pulses.append([New_ID, New_Name, Price, Stock])
    elif Grocery_type == 3:
        product_spices.append([New_ID, New_Name, Price, Stock])
    elif Grocery_type == 4:
        product_cooking_essential.append([New_ID, New_Name, Price, Stock])
    elif Grocery_type == 5:
        product_dairy.append([New_ID, New_Name, Price, Stock])
    elif Grocery_type == 6:
        product_beverages.append([New_ID, New_Name, Price, Stock])
    else:
        print("Invalid Choice")

all_products = (
    products_Grains_Flour
    + products_pulses
    + product_spices
    + product_cooking_essential
    + product_dairy
    + product_beverages
)

def search_grocery():
    print("The Output Will Be In Form Of [Product ID, Product Name, Price, Stock]")
    item_id = int(input("Enter The Item Id (if Not know Type 0 ) : "))

    if item_id == 0:
        print("Searching by Name")
        item_name_found = input("Enter The Name Of The Item: ")
    
        for item in all_products:
            if item[1] == item_name_found:
                print(item)

    else:
        print("Searching by ID")
        for item in all_products:
            if item[0] == item_id:
                print(item)
            

main_menu(user_pin=1234,attempt=3)









    
    
 




                


        
        





