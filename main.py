import tkinter as tk
from form_ui import create_form_ui
from task_display import create_task_table
from db.init_db import init_db


def main():
    try:
        init_db()
    except Exception as e:
        print(f"Note: {e}")

    root = tk.Tk()
    root.title("Smart Task Scheduler")
    root.geometry("900x600")
    root.resizable(True, True)

    tree = create_task_table(root)
    create_form_ui(root, tree)

    root.mainloop()


if __name__ == "__main__":
    main()
