import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import os

tasks_file = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.configure(bg="lightblue")  # Set background color of the main window

        # Task list
        self.tasks = self.load_tasks()
        print(f"Loaded tasks: {self.tasks}")  # Debugging line

        # Frame for the tasks
        self.frame = tk.Frame(root, bg="lightblue")
        self.frame.pack(pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(
            self.frame, width=60, height=10, selectmode=tk.SINGLE, bg="white", fg="black")
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar for the Listbox
        self.scrollbar = tk.Scrollbar(
            self.frame, orient=tk.VERTICAL, command=self.task_listbox.yview, bg="darkblue")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Entry box to add new tasks
        self.task_entry = tk.Entry(root, width=50, bg="white", fg="black")
        self.task_entry.pack(pady=10)

        # Priority dropdown
        self.priority_var = tk.StringVar(root)
        self.priority_var.set("Low")  # default value
        self.priority_menu = tk.OptionMenu(root, self.priority_var, "Low", "Medium", "High")
        self.priority_menu.pack(pady=5)
        
        # Style the OptionMenu
        self.priority_menu.configure(bg="lightgreen", fg="black")
        self.priority_menu["menu"].config(bg="lightgreen", fg="black")
        self.priority_menu["menu"].config(activebackground="darkgreen", activeforeground="white")

        # Buttons
        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task,
                                         bg="purple", fg="white")
        self.add_task_button.pack(pady=5)

        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task,
                                            bg="red", fg="white")
        self.delete_task_button.pack(pady=5)

        self.update_task_button = tk.Button(root, text="Update Task", command=self.update_task,
                                            bg="orange", fg="white")
        self.update_task_button.pack(pady=5)

        # Load tasks into the Listbox
        self.update_task_listbox()

    def load_tasks(self):
        if os.path.exists(tasks_file):
            with open(tasks_file, 'r') as file:
                try:
                    tasks = json.load(file)
                    if isinstance(tasks, list):
                        # Ensure each task is a dictionary with required keys
                        for task in tasks:
                            if not all(key in task for key in ["task", "priority", "deadline"]):
                                return []
                        return tasks
                    else:
                        return []
                except json.JSONDecodeError:
                    return []
        return []

    def save_tasks(self):
        with open(tasks_file, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task != "":
            # Prompt for deadline
            deadline = simpledialog.askstring("Deadline", "Enter the deadline (YYYY-MM-DD):")
            if deadline:
                self.tasks.append({"task": task, "priority": priority, "deadline": deadline})
                self.sort_tasks_by_priority()
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
                self.save_tasks()
            else:
                messagebox.showwarning("Warning", "You must enter a deadline.")
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(task_index)
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            print(f"Processing task: {task}")  # Debugging line
            display_text = f"{task['task']} ({task['priority']}, Due: {task['deadline']})"
            self.task_listbox.insert(tk.END, display_text)

    def sort_tasks_by_priority(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda x: priority_order[x["priority"]])

    def update_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            new_task = self.task_entry.get()
            new_priority = self.priority_var.get()
            if new_task != "":
                # Prompt for new deadline
                new_deadline = simpledialog.askstring("Deadline", "Enter the new deadline (YYYY-MM-DD):")
                if new_deadline:
                    self.tasks[task_index] = {"task": new_task, "priority": new_priority, "deadline": new_deadline}
                    self.sort_tasks_by_priority()
                    self.update_task_listbox()
                    self.task_entry.delete(0, tk.END)
                    self.save_tasks()
                else:
                    messagebox.showwarning("Warning", "You must enter a deadline.")
            else:
                messagebox.showwarning("Warning", "You must enter a task.")
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to update.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
