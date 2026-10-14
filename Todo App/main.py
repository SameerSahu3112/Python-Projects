from database_connection import create_connection_todo
def create_task():
    print("Creating a new task...")
    title = input("Enter task title: ")
    desc = input("Enter task description: ")
    date = input("Enter task due date (YYYY-MM-DD): ")
    conn = create_connection_todo()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (title, description, due_date) VALUES (?, ?, ?)", (title, desc, date))
    conn.commit()
    conn.close()    

def update_task():
    print("Updating an existing task...")
    task_id = input("Enter task ID to update: ")
    title = input("Enter new task title: ")
    desc = input("Enter new task description: ")
    date = input("Enter new task due date (YYYY-MM-DD): ")
    conn = create_connection_todo()
    cursor = conn.cursor()
    cursor.execute("UPDATE todo SET title = ?, description = ?, due_date = ? WHERE id = ?", (title, desc, date, task_id))
    conn.commit()
    conn.close()

def delete_task():
    print("Deleting a task...")
    task_id = input("Enter task ID to delete: ")
    conn = create_connection_todo()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def view_tasks():
    print("Viewing all tasks...")
    conn = create_connection_todo()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo")
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Due Date: {task[3]}")

