import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ttkbootstrap as tb
from datetime import datetime


class TaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Scheduler")
        self.root.geometry("800x600")
        self.style = tb.Style("flatly")  # Light theme

        self.task_data = []

        self.create_widgets()

    def create_widgets(self):
        # ---------- INPUT FRAME ----------
        input_frame = ttk.LabelFrame(
            self.root, text="Add New Task", padding=20)
        input_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Description:").grid(
            row=1, column=0, sticky="w")
        self.desc_entry = ttk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Priority:").grid(
            row=0, column=2, sticky="w")
        self.priority_combo = ttk.Combobox(
            input_frame, values=["High", "Medium", "Low"], state="readonly")
        self.priority_combo.grid(row=0, column=3, padx=10, pady=5)
        self.priority_combo.set("Medium")

        ttk.Label(input_frame, text="Deadline (YYYY-MM-DD):").grid(
            row=1, column=2, sticky="w")
        self.deadline_entry = ttk.Entry(input_frame, width=18)
        self.deadline_entry.grid(row=1, column=3, padx=10, pady=5)
        self.deadline_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(input_frame, text="Duration (mins):").grid(
            row=3, column=0, sticky="w", pady=5)
        self.duration_entry = ttk.Spinbox(
            input_frame, from_=1, to=1440, width=8)
        self.duration_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.duration_entry.set(60)  # Default to 60 minutes

        # Add calendar button
        ttk.Button(
            input_frame,
            text="📅",
            command=self.show_calendar_picker,
            width=3
        ).grid(row=1, column=4, padx=2)

        # ---------- BUTTONS ----------
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=5)

        self.add_btn = ttk.Button(
            button_frame, text="Add Task", command=self.add_task)
        self.add_btn.pack(side="left", padx=10)

        self.edit_btn = ttk.Button(
            button_frame, text="Edit Task", command=self.edit_task)
        self.edit_btn.pack(side="left", padx=10)

        self.delete_btn = ttk.Button(
            button_frame, text="Delete Task", command=self.delete_task)
        self.delete_btn.pack(side="left", padx=10)

        self.clear_btn = ttk.Button(
            search_frame, text="Clear", command=self.load_tasks)
        self.clear_btn.pack(side='left', padx=5)

        # ---------- TASK DISPLAY ----------
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Title", "Description", "Priority", "Deadline")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", stretch=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ---------- STATUS BAR ----------
        self.status_label = ttk.Label(
            self.root, text="Welcome to Smart Task Scheduler!", anchor="center")
        self.status_label.pack(fill="x", pady=5)

    def show_calendar_picker(self):
        """Alternative calendar picker using simpledialog"""
        date_str = simpledialog.askstring(
            "Select Date", "Enter date (YYYY-MM-DD):")
        if date_str:
            try:
                # Validate date format
                datetime.strptime(date_str, "%Y-%m-%d")
                self.deadline_entry.delete(0, tk.END)
                self.deadline_entry.insert(0, date_str)
            except ValueError:
                self.status_label.config(
                    text="Invalid date format (use YYYY-MM-DD)", foreground="red")

    # ---------- DUMMY CALLBACKS (PLACEHOLDERS) ----------
    def add_task(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        priority = self.priority_combo.get()
        deadline = self.deadline_entry.get()
        duration = self.duration_entry.get()

        if not title:
            self.status_label.config(
                text="Title is required!", foreground="red")
            return

        self.tree.insert("", "end", values=(title, desc, priority, deadline))
        self.status_label.config(
            text=f"Task '{title}' added.", foreground="green")
        self.clear_inputs()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            self.status_label.config(
                text="No task selected to edit!", foreground="orange")
            return

        item = self.tree.item(selected)
        values = item["values"]

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[0])
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, values[1])
        self.priority_combo.set(values[2])
        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, str(values[3]))

        self.tree.delete(selected)
        self.status_label.config(
            text="Editing mode: Update fields and press 'Add Task' to re-add.", foreground="blue")

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            self.status_label.config(
                text="No task selected to delete!", foreground="orange")
            return

        for item in selected:
            self.tree.delete(item)
        self.status_label.config(text="Task(s) deleted.", foreground="red")

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.priority_combo.set("Medium")
        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))


# ---------- RUN ----------
if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = TaskSchedulerApp(root)
    root.mainloop()
