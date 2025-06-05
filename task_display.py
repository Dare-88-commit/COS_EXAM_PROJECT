import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from engine import get_all_tasks, search_tasks, get_task_details


def create_task_table(root):
    wrapper = tk.Frame(root)
    wrapper.pack(padx=10, pady=10)

    search_frame = tk.Frame(wrapper)
    search_frame.pack(fill="x", pady=(0, 5))

    search_var = tk.StringVar()

    def handle_search():
        query = search_var.get()
        if query.strip():
            update_tree(tree, search_tasks(query))
        else:
            refresh_tasks(tree)

    tk.Label(search_frame, text="Search:").pack(side="left")
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="Go", command=handle_search).pack(side="left")

    tree = ttk.Treeview(wrapper, columns=(
        "ID", "Title", "Priority", "Deadline", "Days Left"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Priority", text="Priority")
    tree.heading("Deadline", text="Deadline")
    tree.heading("Days Left", text="Days Left")
    tree.column("ID", width=30)
    tree.column("Title", width=150)
    tree.column("Priority", width=80)
    tree.column("Deadline", width=100)
    tree.column("Days Left", width=80)
    tree.pack()

    def show_description(event):
        selected_item = tree.focus()
        if selected_item:
            task_id = tree.item(selected_item)["values"][0]
            task_details = get_task_details(task_id)
            if task_details:
                description = task_details[2]  # Description is at index 2
                messagebox.showinfo("Task Description",
                                    f"Title: {task_details[1]}\n\nDescription:\n{description if description else 'No description available'}")

    tree.bind("<Double-1>", show_description)
    refresh_tasks(tree)
    return tree


def refresh_tasks(tree):
    tasks = get_all_tasks()
    for item in tree.get_children():
        tree.delete(item)
    for task in tasks:
        task_id, title, _, priority, deadline, duration = task
        tree.insert("", "end", values=(task_id, title, priority, deadline, duration),
                    tags=("overdue",) if is_overdue(deadline) else ())


def update_tree(tree, rows):
    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        task_id, title, _, priority, deadline, duration = row
        tree.insert("", "end", values=(task_id, title, priority, deadline, duration),
                    tags=("overdue",) if is_overdue(deadline) else ())


def is_overdue(deadline_str):
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        return deadline.date() < datetime.now().date()
    except:
        return False
