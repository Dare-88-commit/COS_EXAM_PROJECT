import tkinter as tk
from tkinter import ttk, messagebox
from engine import add_task, delete_task, update_task, get_all_tasks, get_task_details
from task_display import refresh_tasks


def create_form_ui(root, tree):
    frame = tk.Frame(root, bg="#f0f0f0", padx=15,
                     pady=15, bd=2, relief=tk.GROOVE)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
    style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
    style.configure("TEntry", padding=5)
    style.map("TButton", background=[("active", "#45a049")])

    ttk.Label(frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
    title_entry = ttk.Entry(frame, width=30, font=("Arial", 10))
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Description:").grid(
        row=1, column=0, sticky="w", pady=5)
    desc_entry = ttk.Entry(frame, width=30, font=("Arial", 10))
    desc_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Priority:").grid(
        row=2, column=0, sticky="w", pady=5)
    priority_var = tk.StringVar(value="Medium")
    priority_menu = ttk.OptionMenu(
        frame, priority_var, "Medium", "Low", "Medium", "High")
    priority_menu.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=3,
                                                         column=0, sticky="w", pady=5)
    deadline_entry = ttk.Entry(frame, width=30, font=("Arial", 10))
    deadline_entry.grid(row=3, column=1, padx=5, pady=5)

    button_frame = tk.Frame(frame, bg="#f0f0f0")
    button_frame.grid(row=4, column=0, columnspan=2, pady=10)

    def clear_form():
        title_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        priority_var.set("Medium")
        deadline_entry.delete(0, tk.END)
        add_btn.config(text="Add Task", command=handle_add,
                       bg="#4CAF50", activebackground="#45a049")

    def get_selected_task_id():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select a task first")
            return None
        return tree.item(selected)["values"][0]

    def handle_add():
        title = title_entry.get()
        desc = desc_entry.get()
        priority = priority_var.get()
        deadline = deadline_entry.get()

        success, msg = add_task(title, desc, priority, deadline)
        messagebox.showinfo("Add Task", msg)
        if success:
            refresh_tasks(tree)
            clear_form()

    def handle_edit():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select a task first")
            return

        try:
            task_id = get_selected_task_id()
            task = get_task_details(task_id)

            if not task:
                messagebox.showerror("Error", "Task not found in database")
                return

            clear_form()
            title_entry.insert(0, task[1])
            desc_entry.insert(0, task[2])
            priority_var.set(task[3])
            deadline_entry.insert(0, task[4])

            add_btn.config(text="Update Task", command=lambda: handle_update(
                task_id), bg="#2196F3", activebackground="#0b7dda")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load task: {str(e)}")

    def handle_update(task_id):
        title = title_entry.get()
        desc = desc_entry.get()
        priority = priority_var.get()
        deadline = deadline_entry.get()

        success, msg = update_task(task_id, title, desc, priority, deadline)
        messagebox.showinfo("Update Task", msg)
        if success:
            refresh_tasks(tree)
            clear_form()

    def handle_delete():
        task_id = get_selected_task_id()
        if not task_id:
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            return

        success, msg = delete_task(task_id)
        messagebox.showinfo("Delete Task", msg)
        if success:
            refresh_tasks(tree)
            clear_form()

    add_btn = tk.Button(button_frame, text="Add Task", command=handle_add, bg="#4CAF50", fg="white", font=(
        "Arial", 10, "bold"), activebackground="#45a049", padx=10, pady=5, bd=0)
    add_btn.pack(side=tk.LEFT, padx=5)

    edit_btn = tk.Button(button_frame, text="Edit Task", command=handle_edit, bg="#FFC107", fg="black", font=(
        "Arial", 10, "bold"), activebackground="#ffab00", padx=10, pady=5, bd=0)
    edit_btn.pack(side=tk.LEFT, padx=5)

    del_btn = tk.Button(button_frame, text="Delete Task", command=handle_delete, bg="#f44336", fg="white", font=(
        "Arial", 10, "bold"), activebackground="#d32f2f", padx=10, pady=5, bd=0)
    del_btn.pack(side=tk.LEFT, padx=5)

    guide_frame = tk.Frame(frame, bg="#f0f0f0", padx=5, pady=5)
    guide_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    guide_text = """Quick Guide:
1. Add Task: Fill fields and click 'Add Task'
2. Edit: Select task > Click 'Edit' > Modify > 'Update Task'
3. Delete: Select task > Click 'Delete'
4. View Description: Double-click any task
5. Search: Type in search box and click 'Go'"""

    guide_label = tk.Label(guide_frame, text=guide_text,
                           bg="#f0f0f0", fg="#333333",
                           font=("Arial", 9), justify="left",
                           anchor="w", padx=10, pady=5)
    guide_label.pack(fill="x")

    return frame
