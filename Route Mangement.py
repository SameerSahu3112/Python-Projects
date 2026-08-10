from Connection import create_connection_route    
db = create_connection_route()
cursor = db.cursor()

# ---------- DRIVER ----------
def add_driver():
    name = input("Name: ")
    license = input("License: ")
    phone = input("Phone: ")
    cursor.execute("INSERT INTO drivers(name, license_no, phone) VALUES (%s,%s,%s)", (name, license, phone))
    db.commit()

def view_drivers():
    cursor.execute("SELECT * FROM drivers")
    for row in cursor.fetchall():
        print(row)

def update_driver():
    id = input("Driver ID: ")
    name = input("New Name: ")
    cursor.execute("UPDATE drivers SET name=%s WHERE id=%s", (name, id))
    db.commit()

def delete_driver():
    id = input("Driver ID: ")
    cursor.execute("DELETE FROM drivers WHERE id=%s", (id,))
    db.commit()

# ---------- BUS ----------
def add_bus():
    number = input("Bus Number: ")
    cap = input("Capacity: ")
    cursor.execute("INSERT INTO buses(bus_number, capacity) VALUES (%s,%s)", (number, cap))
    db.commit()

def view_buses():
    cursor.execute("SELECT * FROM buses")
    for row in cursor.fetchall():
        print(row)

def update_bus():
    id = input("Bus ID: ")
    cap = input("New Capacity: ")
    cursor.execute("UPDATE buses SET capacity=%s WHERE id=%s", (cap, id))
    db.commit()

def delete_bus():
    id = input("Bus ID: ")
    cursor.execute("DELETE FROM buses WHERE id=%s", (id,))
    db.commit()

# ---------- ROUTE ----------
def add_route():
    src = input("Source: ")
    dst = input("Destination: ")
    dist = input("Distance: ")
    cursor.execute("INSERT INTO routes(source, destination, distance_km) VALUES (%s,%s,%s)", (src, dst, dist))
    db.commit()

def view_routes():
    cursor.execute("SELECT * FROM routes")
    for row in cursor.fetchall():
        print(row)

def update_route():
    id = input("Route ID: ")
    dist = input("New Distance: ")
    cursor.execute("UPDATE routes SET distance_km=%s WHERE id=%s", (dist, id))
    db.commit()

def delete_route():
    id = input("Route ID: ")
    cursor.execute("DELETE FROM routes WHERE id=%s", (id,))
    db.commit()

# ---------- ASSIGNMENT ----------
def add_assignment():
    r = input("Route ID: ")
    d = input("Driver ID: ")
    b = input("Bus ID: ")
    cursor.execute("INSERT INTO assignments(route_id, driver_id, bus_id) VALUES (%s,%s,%s)", (r, d, b))
    db.commit()

def view_assignments():
    query = """
    SELECT a.id, r.source, r.destination, d.name, b.bus_number
    FROM assignments a
    JOIN routes r ON a.route_id = r.id
    JOIN drivers d ON a.driver_id = d.id
    JOIN buses b ON a.bus_id = b.id
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

def update_assignment():
    id = input("Assignment ID: ")
    new_driver = input("New Driver ID: ")
    cursor.execute("UPDATE assignments SET driver_id=%s WHERE id=%s", (new_driver, id))
    db.commit()

def delete_assignment():
    id = input("Assignment ID: ")
    cursor.execute("DELETE FROM assignments WHERE id=%s", (id,))
    db.commit()

# ---------- DRIVER MENU ----------

def driver_menu():
    while True:
        print("\n========== DRIVER MANAGEMENT ==========")
        print("1. Add Driver")
        print("2. View Drivers")
        print("3. Update Driver")
        print("4. Delete Driver")
        print("0. Back")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_driver()
            elif choice == 2:
                view_drivers()
            elif choice == 3:
                update_driver()
            elif choice == 4:
                delete_driver()
            elif choice == 0:
                break
            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter a valid number!")


# ---------- BUS MENU ----------

def bus_menu():
    while True:
        print("\n========== BUS MANAGEMENT ==========")
        print("1. Add Bus")
        print("2. View Buses")
        print("3. Update Bus")
        print("4. Delete Bus")
        print("0. Back")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_bus()
            elif choice == 2:
                view_buses()
            elif choice == 3:
                update_bus()
            elif choice == 4:
                delete_bus()
            elif choice == 0:
                break
            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter a valid number!")


# ---------- ROUTE MENU ----------

def route_menu():
    while True:
        print("\n========== ROUTE MANAGEMENT ==========")
        print("1. Add Route")
        print("2. View Routes")
        print("3. Update Route")
        print("4. Delete Route")
        print("0. Back")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_route()
            elif choice == 2:
                view_routes()
            elif choice == 3:
                update_route()
            elif choice == 4:
                delete_route()
            elif choice == 0:
                break
            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter a valid number!")


# ---------- ASSIGNMENT MENU ----------

def assignment_menu():
    while True:
        print("\n========== ASSIGNMENT MANAGEMENT ==========")
        print("1. Add Assignment")
        print("2. View Assignments")
        print("3. Update Assignment")
        print("4. Delete Assignment")
        print("0. Back")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_assignment()
            elif choice == 2:
                view_assignments()
            elif choice == 3:
                update_assignment()
            elif choice == 4:
                delete_assignment()
            elif choice == 0:
                break
            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter a valid number!")


# ---------- MAIN MENU ----------

while True:

    print("\n==========================================")
    print("       ROUTE MANAGEMENT SYSTEM")
    print("==========================================")
    print("1. Driver Management")
    print("2. Bus Management")
    print("3. Route Management")
    print("4. Assignment Management")
    print("0. Exit")
    print("==========================================")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            driver_menu()

        elif choice == 2:
            bus_menu()

        elif choice == 3:
            route_menu()

        elif choice == 4:
            assignment_menu()

        elif choice == 0:
            print("\nThank you for using Route Management System!")
            break

        else:
            print("Invalid choice!")

    except ValueError:
        print("Please enter a valid number!")