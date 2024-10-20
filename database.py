import sqlite3
from datetime import datetime, timedelta

DATABASE_NAME = 'tasks.db'


def init_db():
    '''create database if it doesn't exist, adding table for tasks'''
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            user TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_task_to_db(description, due_date, user):
    '''Function for adding a new task'''
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    status = "incomplete"
    cursor.execute('INSERT INTO tasks (description, date, status, user) VALUES (?, ?, ?, ?)',
                   (description, due_date, status, user))
    conn.commit()
    conn.close()


def get_tasks_from_db(user):
    '''Function for getting all the tasks'''
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user = ?', (user,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def get_task_from_db(task_id, user):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ? AND user = ?', (task_id, user))
    task = cursor.fetchone()
    conn.close()
    return task


def update_task_in_db(task_id, description, due_date, status, user):
    '''Function for updating task with task_id'''
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET description = ?, date = ?, status = ? WHERE id = ? AND user = ?',
                   (description, due_date, status, task_id, user))
    conn.commit()
    conn.close()


def delete_task_from_db(task_id, user):
    '''Function for deliting the task with task_id'''
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ? AND user = ?', (task_id, user))
    task = cursor.fetchone()
    cursor.execute('DELETE FROM tasks WHERE id = ? AND user = ?', (task_id, user))
    conn.commit()
    conn.close()
    return task


def find_reminders():
    '''function for finding tasks with deadline'''
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    cursor.execute("SELECT * FROM tasks WHERE date = ?", (tomorrow,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks
