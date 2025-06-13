import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import ttkbootstrap as tb
from db.init_db import init_db
from db.connection import get_connection
from datetime import datetime


class TaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Scheduler - Pan-Atlantic University")
        self.root.geometry("1000x700")
        self.style = tb.Style("flatly")

        # Initialize database
        try:
            init_db()
            test_conn = get_connection()
            test_conn.close()
            print("Database connected successfully!")
            self.db_connected = True
        except Exception as e:
            print(f"Database error: {e}")
            self.db_connected = False

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        input_frame = ttk.LabelFrame(
            main_frame, text="Task Details", padding=10)
        input_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(input_frame, text="Title:").grid(
            row=0, column=0, sticky="w", pady=5)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=3,
                              padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Description:").grid(
            row=1, column=0, sticky="nw", pady=5)
        self.desc_text = tk.Text(input_frame, height=4, width=40, wrap=tk.WORD)
        self.desc_text.grid(row=1, column=1, columnspan=3,
                            padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Priority:").grid(
            row=2, column=0, sticky="w", pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = ttk.OptionMenu(
            input_frame, self.priority_var, "Medium", "Low", "Medium", "High")
        priority_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=2,
                                                                                column=2, sticky="w", pady=5)
        self.deadline_entry = ttk.Entry(input_frame, width=15)
        self.deadline_entry.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        self.deadline_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

        ttk.Button(input_frame, text="📅", command=self.show_datetime_picker,
                   width=3).grid(row=2, column=4, padx=2)

        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=3, column=0, columnspan=5, pady=10, sticky="ew")

        self.add_btn = ttk.Button(
            btn_frame, text="Add Task", command=self.add_task)
        self.add_btn.pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Edit Task",
                   command=self.edit_task).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Task",
                   command=self.delete_task).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Toggle Complete",
                   command=self.toggle_selected_task_completion).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Clear Fields",
                   command=self.clear_fields).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Refresh",
                   command=self.load_tasks).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Help",
                   command=self.show_help).pack(side="left", padx=5)

        list_frame = ttk.LabelFrame(main_frame, text="Task List", padding=10)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        columns = ("ID", "Title", "Priority", "Deadline", "Time Remaining", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50)
            elif col == "Title":
                self.tree.column(col, width=180)
            elif col == "Deadline":
                self.tree.column(col, width=120)
            elif col == "Time Remaining":
                self.tree.column(col, width=120)
            elif col == "Status":
                self.tree.column(col, width=80)
            else:
                self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind events
        self.tree.bind("<Double-1>", self.show_task_description)
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right-click

        # Search Frame
        search_frame = ttk.LabelFrame(
            main_frame, text="Search Tasks", padding=5)
        search_frame.pack(fill="x", pady=(0, 10))

        self.search_var = tk.StringVar()
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        search_entry = ttk.Entry(
            search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)

        ttk.Button(search_frame, text="Search",
                   command=self.search_tasks).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Clear",
                   command=self.clear_search).pack(side="left", padx=5)

        # Bind Enter key to search
        search_entry.bind("<Return>", lambda e: self.search_tasks())

        # Task Statistics Frame
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill="x", pady=(0, 5))

        self.stats_var = tk.StringVar(
            value="Total: 0 | Pending: 0 | Completed: 0 | Overdue: 0")
        stats_label = ttk.Label(
            stats_frame, textvariable=self.stats_var, font=("Arial", 9))
        stats_label.pack(side="left")

        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x")

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side="left")

        input_frame.columnconfigure(1, weight=1)

        # Keyboard shortcuts
        self.root.bind("<F5>", lambda e: self.load_tasks())  # F5 to refresh
        # Ctrl+N for new task
        self.root.bind("<Control-n>", lambda e: self.clear_fields())
        # Delete key to delete selected task
        self.root.bind("<Delete>", lambda e: self.delete_task())
        # Space to toggle completion
        self.root.bind(
            "<space>", lambda e: self.toggle_selected_task_completion())

    def calculate_time_remaining(self, deadline_str):
        """Calculate time remaining until deadline in days, hours, minutes format"""
        if not deadline_str:
            return "No deadline"
        
        try:
            from datetime import datetime
            deadline = datetime.fromisoformat(str(deadline_str))
            now = datetime.now()
            
            if deadline < now:
                # Past deadline
                diff = now - deadline
                return f"Overdue by {self.format_duration(diff)}"
            else:
                # Future deadline
                diff = deadline - now
                return self.format_duration(diff)
        except:
            return "Invalid date"
    
    def format_duration(self, duration):
        """Format a timedelta into days, hours, minutes"""
        total_seconds = int(duration.total_seconds())
        
        if total_seconds <= 0:
            return "0 minutes"
        
        days = total_seconds // 86400  # 86400 seconds in a day
        hours = (total_seconds % 86400) // 3600  # 3600 seconds in an hour
        minutes = (total_seconds % 3600) // 60
        
        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0 or not parts:  # Show minutes if no other parts or if there are minutes
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        
        return ", ".join(parts)

    def get_db_connection(self):
        """Get a fresh database connection"""
        try:
            return get_connection()
        except Exception as e:
            print(f"Database connection error: {e}")
            self.status_var.set(f"Database connection error: {e}")
            return None

    def show_datetime_picker(self):
        from tkinter import simpledialog
        datetime_str = simpledialog.askstring(
            "Select Date & Time", "Enter datetime (YYYY-MM-DD HH:MM):")
        if datetime_str:
            try:
                datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                self.deadline_entry.delete(0, tk.END)
                self.deadline_entry.insert(0, datetime_str)
            except ValueError:
                self.status_var.set("Invalid datetime format (use YYYY-MM-DD HH:MM)")

    def load_tasks(self):
        if not self.db_connected:
            self.status_var.set("Database not connected")
            return

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, priority, deadline, completed FROM tasks")
            for item in self.tree.get_children():
                self.tree.delete(item)
            for task in cursor.fetchall():
                status = "✓ Completed" if task[4] else "⚬ Pending"  # completed is now at index 4
                
                # Calculate time remaining automatically
                time_remaining = self.calculate_time_remaining(task[3])  # deadline at index 3
                
                # Add color coding for overdue tasks
                tags = ()
                if not task[4] and task[3]:  # Not completed and has deadline
                    try:
                        from datetime import datetime
                        deadline_dt = datetime.fromisoformat(str(task[3]))
                        if deadline_dt < datetime.now():
                            tags = ("overdue",)
                            status = "⚠ Overdue"
                    except:
                        pass
                elif task[4]:  # Completed tasks
                    tags = ("completed",)

                # Format datetime for display (show first 16 chars: YYYY-MM-DD HH:MM)
                deadline_display = str(task[3])[:16] if task[3] else "N/A"
                
                self.tree.insert("", "end", values=(
                    task[0], task[1], task[2], deadline_display, time_remaining, status), tags=tags)

            # Configure tags for visual feedback
            self.tree.tag_configure("overdue", background="#ffcccc")
            self.tree.tag_configure("completed", background="#ccffcc")
            self.status_var.set("Tasks loaded successfully")
        except Exception as e:
            self.status_var.set(f"Error loading tasks: {str(e)}")
        finally:
            conn.close()

        # Update statistics after loading
        self.update_task_statistics()

    def sort_tasks(self, sort_by):
        items = [(self.tree.item(item)['values'], item)
                 for item in self.tree.get_children()]

        if sort_by == "priority":
            # Sort by priority (High, Medium, Low)
            priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
            items.sort(key=lambda x: priority_order.get(
                x[0][2], 4))  # Default to 4 if missing

        elif sort_by == "urgency":
            # Sort by deadline proximity (nearest first)
            today = datetime.now().date()

            def urgency_key(x):
                try:
                    deadline = datetime.strptime(x[0][3], "%Y-%m-%d").date()
                    return (deadline - today).days
                except (ValueError, IndexError):
                    return float('inf')  # Push invalid/missing dates to bottom

            items.sort(key=urgency_key)

        # Clear the current tree and reinsert sorted items
        for item in self.tree.get_children():
            self.tree.delete(item)

        for values, _ in items:
            self.tree.insert('', 'end', values=values)

        for index, (values, item) in enumerate(items):
            self.tree.move(item, "", index)

    def show_task_description(self, event):
        """Show task description when double-clicked"""
        selected = self.tree.selection()
        if not selected:
            return

        task_id = self.tree.item(selected)["values"][0]

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT title, description FROM tasks WHERE id = %s", (task_id,))
            task = cursor.fetchone()

            if task:
                title, description = task
                from tkinter import messagebox
                messagebox.showinfo(
                    "Task Description",
                    f"Title: {title}\n\nDescription:\n{description if description else 'No description available'}"
                )
        except Exception as e:
            self.status_var.set(f"Error loading task description: {str(e)}")

    def show_context_menu(self, event):
        """Show right-click context menu"""
        selected = self.tree.selection()
        if not selected:
            return

        # Create context menu
        context_menu = tk.Menu(self.root, tearoff=0)

        # Get task status
        task_values = self.tree.item(selected)["values"]
        current_status = task_values[5]  # Status is at index 5

        if "Completed" in current_status:
            context_menu.add_command(label="Mark as Pending",
                                     command=lambda: self.toggle_task_completion(selected[0], False))
        else:
            context_menu.add_command(label="Mark as Completed",
                                     command=lambda: self.toggle_task_completion(selected[0], True))

        context_menu.add_separator()
        context_menu.add_command(label="Edit Task", command=self.edit_task)
        context_menu.add_command(label="Delete Task", command=self.delete_task)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def toggle_task_completion(self, item_id, completed):
        """Toggle task completion status"""
        task_id = self.tree.item(item_id)["values"][0]

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET completed = %s WHERE id = %s", (completed, task_id))
            conn.commit()

            status = "Completed" if completed else "Pending"
            self.status_var.set(f"Task marked as {status.lower()}")
            self.load_tasks()  # Refresh the display

        except Exception as e:
            self.status_var.set(f"Error updating task: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def toggle_selected_task_completion(self):
        """Toggle completion status of selected task via button"""
        selected = self.tree.selection()
        if not selected:
            self.status_var.set("Error: No task selected")
            return

        # Get current task status
        task_values = self.tree.item(selected[0])["values"]
        current_status = task_values[5]  # Status is at index 5

        # Toggle the completion status
        new_completed_status = "Completed" not in current_status

        self.toggle_task_completion(selected[0], new_completed_status)

    def clear_search(self):
        """Clear search and show all tasks"""
        self.search_var.set("")
        self.load_tasks()
        self.status_var.set("Showing all tasks")

    def update_task_statistics(self):
        """Update task statistics display"""
        if not self.db_connected:
            return

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()

            # Get total tasks
            cursor.execute("SELECT COUNT(*) FROM tasks")
            total = cursor.fetchone()[0]

            # Get completed tasks
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = true")
            completed = cursor.fetchone()[0]

            # Get pending tasks
            pending = total - completed

            # Get overdue tasks
            cursor.execute("""
                SELECT COUNT(*) FROM tasks 
                WHERE completed = false AND deadline < CURRENT_DATE
            """)
            overdue = cursor.fetchone()[0]

            self.stats_var.set(
                f"Total: {total} | Pending: {pending} | Completed: {completed} | Overdue: {overdue}")

        except Exception as e:
            self.stats_var.set("Statistics unavailable")
        finally:
            conn.close()

    def show_help(self):
        """Show help dialog with usage instructions"""
        from tkinter import messagebox
        help_text = """TASK COMPLETION HELP:

How to mark tasks as completed:

1. TOGGLE COMPLETE BUTTON:
   • Select a task in the list
   • Click "Toggle Complete" button

2. RIGHT-CLICK MENU:
   • Right-click on any task
   • Choose "Mark as Completed" or "Mark as Pending"

3. KEYBOARD SHORTCUT:
   • Select a task
   • Press SPACEBAR to toggle completion

VISUAL INDICATORS:
✓ Green background = Completed tasks
⚠ Red background = Overdue tasks  
⚬ Normal = Pending tasks

OTHER SHORTCUTS:
• F5 = Refresh tasks
• Ctrl+N = New task
• Delete = Delete selected task
• Double-click = View description"""

        messagebox.showinfo("Help - Task Completion", help_text)

    def search_tasks(self):
        """Search tasks by title or description"""
        query = self.search_var.get().strip()
        if not query:
            self.status_var.set("Please enter a search term")
            return

        if not self.db_connected:
            self.status_var.set("Database not connected")
            return

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute("""
                SELECT id, title, priority, deadline, completed 
                FROM tasks 
                WHERE title ILIKE %s OR description ILIKE %s
                ORDER BY deadline
            """, (search_term, search_term))

            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Add search results to treeview
            results = cursor.fetchall()
            for task in results:
                status = "✓ Completed" if task[4] else "⚬ Pending"  # completed is now at index 4
                
                # Calculate time remaining automatically
                time_remaining = self.calculate_time_remaining(task[3])  # deadline at index 3
                
                # Add color coding for overdue tasks
                tags = ()
                if not task[4] and task[3]:  # Not completed and has deadline
                    try:
                        from datetime import datetime
                        deadline_dt = datetime.fromisoformat(str(task[3]))
                        if deadline_dt < datetime.now():
                            tags = ("overdue",)
                            status = "⚠ Overdue"
                    except:
                        pass
                elif task[4]:  # Completed tasks
                    tags = ("completed",)

                # Format datetime for display
                deadline_display = str(task[3])[:16] if task[3] else "N/A"

                self.tree.insert("", "end", values=(
                    task[0], task[1], task[2], deadline_display, time_remaining, status), tags=tags)

            self.status_var.set(
                f"Found {len(results)} task(s) matching '{query}'")

            # Configure tags for visual feedback
            self.tree.tag_configure("overdue", background="#ffcccc")

        except Exception as e:
            self.status_var.set(f"Error searching tasks: {str(e)}")
        finally:
            conn.close()

    def add_task(self):
        if not self.db_connected:
            self.status_var.set("Database not connected")
            return

        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        deadline = self.deadline_entry.get()

        if not title:
            self.status_var.set("Error: Title is required")
            return

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, description, priority, deadline, completed) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (title, description, priority, deadline, False)
            )
            conn.commit()
            self.status_var.set(f"Task '{title}' added successfully")
            self.clear_fields()
            self.load_tasks()
        except Exception as e:
            self.status_var.set(f"Database error: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            self.status_var.set("Error: No task selected")
            return

        task_id = self.tree.item(selected)["values"][0]
        
        conn = self.get_db_connection()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, description, priority, deadline FROM tasks WHERE id = %s", (task_id,))
            task = cursor.fetchone()

            if task:
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, task[0])
                self.desc_text.delete("1.0", tk.END)
                self.desc_text.insert("1.0", task[1])
                self.priority_var.set(task[2])
                
                # Set the datetime picker
                self.deadline_entry.delete(0, tk.END)
                self.deadline_entry.insert(0, str(task[3])[:16] if task[3] else "")
                self.add_btn.config(text="Update Task",
                                    command=lambda: self.update_task(task_id))
                self.status_var.set(f"Editing Task ID: {task_id}")
        except Exception as e:
            self.status_var.set(f"Error loading task: {str(e)}")
        finally:
            conn.close()

    def update_task(self, task_id):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        deadline = self.deadline_entry.get()

        if not title:
            self.status_var.set("Error: Title is required")
            return

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET title=%s, description=%s, priority=%s, deadline=%s WHERE id=%s",
                (title, description, priority, deadline, task_id)
            )
            conn.commit()
            self.status_var.set(f"Task '{title}' updated successfully")
            self.clear_fields()
            self.add_btn.config(text="Add Task", command=self.add_task)
            self.load_tasks()
        except Exception as e:
            self.status_var.set(f"Error updating task: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            self.status_var.set("Error: No task selected")
            return

        task_id = self.tree.item(selected)["values"][0]

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()
            self.status_var.set("Task deleted successfully")
            self.load_tasks()
        except Exception as e:
            self.status_var.set(f"Error deleting task: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.priority_var.set("Medium")
        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.add_btn.config(text="Add Task", command=self.add_task)
        self.status_var.set("Ready")


if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = TaskSchedulerApp(root)
    root.mainloop()
