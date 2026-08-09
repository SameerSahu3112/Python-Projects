import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hda77063",
    database="route_management"
)

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

# ---------- MENU ----------
while True:
    print("\n1.Driver Add 2.View 3.Update 4.Delete")
    print("5.Bus Add 6.View 7.Update 8.Delete")
    print("9.Route Add 10.View 11.Update 12.Delete")
    print("13.Assign 14.View 15.Update 16.Delete")
    print("0.Exit")

    ch = input("Choice: ")

    if ch == "1": add_driver()
    elif ch == "2": view_drivers()
    elif ch == "3": update_driver()
    elif ch == "4": delete_driver()

    elif ch == "5": add_bus()
    elif ch == "6": view_buses()
    elif ch == "7": update_bus()
    elif ch == "8": delete_bus()

    elif ch == "9": add_route()
    elif ch == "10": view_routes()
    elif ch == "11": update_route()
    elif ch == "12": delete_route()

    elif ch == "13": add_assignment()
    elif ch == "14": view_assignments()
    elif ch == "15": update_assignment()
    elif ch == "16": delete_assignment()

    elif ch == "0":
        print("Exit")
        break
