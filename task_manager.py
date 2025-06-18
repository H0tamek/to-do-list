# Class for working with tasks

import json
import os

class TaskManager:
    def __init__(self):
        # Make sure the file exists
        if not os.path.exists('task.json'):
            with open('task.json', 'w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False, indent=4)
        
    def view_tasks(self):
        # Display all tasks
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            for task in tasks:
                print(f"ID: {task['id']}, Text: {task['text']}, Status: {task['status']}")
            print()
    
    def add_task(self):
        # Add a new task
        text = input("Enter task text: ")
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = max([task['id'] for task in tasks], default=0) + 1
            tasks.append({'id': task_id, 'text': text, 'status': 'In Progress'})
        with open('task.json', 'w', encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
        print("Task successfully added.\n")
    
    def edit_task(self):
        # Edit existing task
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Enter the ID of the task you want to edit: "))
            for task in tasks:
                if task['id'] == task_id:
                    new_text = input("Enter new task text: ")
                    task['text'] = new_text
                    task['status'] = 'In Progress'
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Task successfully modified.\n")
                    return
    
    def delete_task(self):
        # Delete a task
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Enter the ID of the task you want to delete: "))
            for task in tasks:
                if task['id'] == task_id:
                    tasks.remove(task)
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Task successfully deleted.\n")
                    return

    def mark_task_completed(self):
        # Mark task as completed
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Enter the ID of the task you want to mark as completed: "))
            for task in tasks:
                if task['id'] == task_id:
                    task['status'] = 'Completed'
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Task successfully marked as completed.\n")
                    return
    
    def mark_task_not_completed(self):
        # Mark task as not completed
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Enter the ID of the task you want to mark as not completed: "))
            for task in tasks:
                if task['id'] == task_id:
                    task['status'] = 'Not Completed'
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Task successfully marked as not completed.\n")
                    return