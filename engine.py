import psycopg2
from db.connection import get_connection
from datetime import datetime


def validate_task(title, description, priority, deadline):
    if not title.strip():
        return False, "Title cannot be empty."
    if priority not in ["Low", "Medium", "High"]:
        return False, "Priority must be Low, Medium, or High."
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        return False, "Deadline must be in YYYY-MM-DD format."
    return True, "Valid input."


def add_task(title, description, priority, deadline):
    is_valid, message = validate_task(title, description, priority, deadline)
    if not is_valid:
        return False, message

    # Calculate duration
    from datetime import datetime
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    today = datetime.now().date()
    duration = (deadline_date - today).days

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO tasks (title, description, priority, deadline, duration)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (title, description, priority, deadline, duration))
        conn.commit()
        return True, "Task added successfully."
    except psycopg2.Error as e:
        return False, f"Database error: {e}"
    finally:
        cur.close()
        conn.close()


def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        cur.execute("""
            UPDATE tasks SET id = new_id
            FROM (
                SELECT id, ROW_NUMBER() OVER (ORDER BY id) as new_id 
                FROM tasks
            ) as renumbered
            WHERE tasks.id = renumbered.id
        """)
        conn.commit()
        return True, "Task deleted successfully."
    except psycopg2.Error as e:
        return False, f"Database error: {e}"
    finally:
        cur.close()
        conn.close()


def get_all_tasks():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, title, description, priority, deadline, duration 
            FROM tasks 
            ORDER BY created_at
        """)
        return cur.fetchall()
    except psycopg2.Error as e:
        return []
    finally:
        cur.close()
        conn.close()


def search_tasks(keyword):
    conn = get_connection()
    cur = conn.cursor()
    try:
        search_term = f"%{keyword}%"
        cur.execute("""
            SELECT id, title, description, priority, deadline, duration
            FROM tasks
            WHERE title ILIKE %s OR description ILIKE %s
            ORDER BY deadline
        """, (search_term, search_term))
        return cur.fetchall()
    except psycopg2.Error:
        return []
    finally:
        cur.close()
        conn.close()


def update_task(task_id, title, description, priority, deadline):
    is_valid, message = validate_task(title, description, priority, deadline)
    if not is_valid:
        return False, message

    today = datetime.now().date()
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    duration = (deadline_date - today).days

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE tasks 
            SET title = %s, description = %s, priority = %s, deadline = %s, duration = %s
            WHERE id = %s
        """, (title, description, priority, deadline, duration, task_id))
        conn.commit()
        return True, "Task updated successfully"
    except psycopg2.Error as e:
        return False, f"Database error: {e}"
    finally:
        cur.close()
        conn.close()


def get_task_details(task_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, title, description, priority, deadline, duration 
            FROM tasks WHERE id = %s
        """, (task_id,))
        task = cur.fetchone()
        return task if task else None
    except psycopg2.Error:
        return None
    finally:
        cur.close()
        conn.close()
