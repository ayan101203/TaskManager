import sqlite3
import datetime

# Connect to SQLite database
def connect_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        status TEXT CHECK(status IN ('Pending', 'Completed')) NOT NULL DEFAULT 'Pending'
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS task_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_id INTEGER,
                        title TEXT,
                        description TEXT,
                        status TEXT,
                        timestamp TEXT,
                        FOREIGN KEY (task_id) REFERENCES tasks(id)
                    )''')
    
    conn.commit()
    return conn, cursor

# Add Task
def add_task(title, description):
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
    conn.commit()
    print("Task added successfully!")
    conn.close()

# Edit Task
def edit_task(task_id, new_title, new_description):
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute("INSERT INTO task_history (task_id, title, description, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (task_id, task[1], task[2], task[3], datetime.datetime.now()))
        cursor.execute("UPDATE tasks SET title = ?, description = ? WHERE id = ?", (new_title, new_description, task_id))
        conn.commit()
        print("Task updated successfully!")
    else:
        print("Task not found!")
    conn.close()

# Complete Task
def complete_task(task_id):
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute("INSERT INTO task_history (task_id, title, description, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (task_id, task[1], task[2], task[3], datetime.datetime.now()))
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        conn.commit()
        print("Task marked as completed!")
    else:
        print("Task not found!")
    conn.close()

# View All Tasks
def view_tasks():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    print("\nTask List:")
    for task in tasks:
        print(f"[{task[0]}] {task[1]} - {task[3]}")
    conn.close()

# View Task History
def view_task_history():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM task_history")
    history = cursor.fetchall()
    print("\nTask History:")
    for record in history:
        print(f"[{record[1]}] {record[2]} - {record[4]} ({record[5]})")
    conn.close()

# CLI Menu
def main():
    while True:
        print("""
        Task Management CLI Tool:
        1. Add Task
        2. Edit Task
        3. Complete Task
        4. View Tasks
        5. View Task History
        6. Exit
        """)
        choice = input("Enter your choice: ")
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            add_task(title, description)
        elif choice == '2':
            task_id = int(input("Enter task ID to edit: "))
            new_title = input("Enter new title: ")
            new_description = input("Enter new description: ")
            edit_task(task_id, new_title, new_description)
        elif choice == '3':
            task_id = int(input("Enter task ID to complete: "))
            complete_task(task_id)
        elif choice == '4':
            view_tasks()
        elif choice == '5':
            view_task_history()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    main()
