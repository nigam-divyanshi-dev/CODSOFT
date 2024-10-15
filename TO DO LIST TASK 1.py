import tkinter as tk
from tkinter import messagebox
import pickle

def add_task():
    task = entry.get()
    if task != "":
        listbox.insert(tk.END, task)
        tasks.append({"task": task, "completed": False})
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task")
    refresh_listbox()
    update_status()
    save_tasks()

def delete_task():
    try:
        task_index = listbox.curselection()[0]
        listbox.delete(task_index)
        del tasks[task_index]
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task")
    refresh_listbox()
    update_status()
    save_tasks()

def mark_complete():
    try:
        task_index = listbox.curselection()[0]
        task = tasks[task_index]
        if not task["completed"]:
            task["completed"] = True
            listbox.itemconfig(task_index, {'fg': 'green'})  
            listbox.delete(task_index)
            listbox.insert(task_index, f"{task['task']} (Completed)")
        refresh_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task")
    update_status()

def update_task():
    try:
        task_index = listbox.curselection()[0]
        new_task_text = entry.get()
        if new_task_text != "":
            tasks[task_index]["task"] = new_task_text
            listbox.delete(task_index)
            task_text = f"{new_task_text} (Completed)" if tasks[task_index]["completed"] else new_task_text
            listbox.insert(task_index, task_text)
            if tasks[task_index]["completed"]:
                listbox.itemconfig(task_index, {'fg': 'green'})
            entry.delete(0, tk.END)
            refresh_listbox()
            save_tasks()
        else:
            messagebox.showwarning("Input Error", "Enter a new task description")
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a task to update")

def update_status():
    completed_count = sum(task["completed"] for task in tasks)
    pending_count = len(tasks) - completed_count
    status_label.config(text=f"Pending: {pending_count} | Completed: {completed_count}")

def load_tasks():
    try:
        with open("tasks.pkl", "rb") as f:
            global tasks
            tasks = pickle.load(f)
            for task in tasks:
                task_text = f"{task['task']} (Completed)" if task["completed"] else task["task"]
                listbox.insert(tk.END, task_text)
                if task["completed"]:
                    listbox.itemconfig(tk.END, {'fg': 'green'})  
            refresh_listbox()
        update_status()
    except FileNotFoundError:
        tasks = []

def save_tasks():
    with open("tasks.pkl", "wb") as f:
        pickle.dump(tasks, f)

def refresh_listbox():
    listbox.delete(0, tk.END)  # Clear the listbox
    for index, task in enumerate(tasks, start=1):  # Enumerate tasks with numbering
        task_text = f"{index}. {task['task']} (Completed)" if task["completed"] else f"{index}. {task['task']}"
        listbox.insert(tk.END, task_text)  # Insert task with its number
        if task["completed"]:
            listbox.itemconfig(tk.END, {'fg': 'green'})  # Set completed task color to green


# GUI setup
root = tk.Tk()
root.title("Enhanced To-Do List with Update and Tracking")

# Entry widget to add/update tasks
entry = tk.Entry(root, width=40)
entry.pack()

# Listbox to display tasks
listbox = tk.Listbox(root, height=20, width=70,background = "light yellow",font = "Helvetica")
listbox.pack()

# Buttons for task management
add_button = tk.Button(root, text="Add Task", width=50, background = "light green",command=add_task)
add_button.pack()

delete_button = tk.Button(root, text="Delete Task", width=50, background = "red", command=delete_task)
delete_button.pack()

complete_button = tk.Button(root, text="Mark as Completed", width=50,background = "light blue", command=mark_complete)
complete_button.pack()

update_button = tk.Button(root, text="Update Task", width=50,background = "light pink", command=update_task)
update_button.pack()

# Status label to track the number of pending and completed tasks
status_label = tk.Label(root, text="Pending: 0 | Completed: 0")
status_label.pack()

# Load tasks when the application starts
load_tasks()

# Start the main event loop
root.mainloop()