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
        try:
            # Display all tasks
            with open('task.json', 'r', encoding="utf-8") as file:
                tasks = json.load(file)
                for task in tasks:
                    print(f"ID: {task['id']}, Text: {task['text']}, Status: {task['status']}")
                print()
        except FileNotFoundError:
            print("Task file not found.\n")
        except json.JSONDecodeError:
            print("Error reading task file: Invalid JSON format.\n")
        except Exception as e:
            print(f"Error viewing tasks: {e}\n")
    
    def add_task(self):
        try:
            # Add a new task
            text = input("Enter task text: ")
            with open('task.json', 'r', encoding="utf-8") as file:
                tasks = json.load(file)
                task_id = max([task['id'] for task in tasks], default=0) + 1
                tasks.append({'id': task_id, 'text': text, 'status': 'In Progress'})
            with open('task.json', 'w', encoding="utf-8") as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
            print("Task successfully added.\n")
        except FileNotFoundError:
            print("Task file not found.\n")
        except json.JSONDecodeError:
            print("Error reading task file: Invalid JSON format.\n")
        except Exception as e:
            print(f"Error adding task: {e}\n")
    
    def edit_task(self):
        try:
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
                print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except FileNotFoundError:
            print("Task file not found.\n")
        except json.JSONDecodeError:
            print("Error reading task file: Invalid JSON format.\n")
        except Exception as e:
            print(f"Error editing task: {e}\n")
    
    def delete_task(self):
        try:
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
                print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except FileNotFoundError:
            print("Task file not found.\n")
        except json.JSONDecodeError:
            print("Error reading task file: Invalid JSON format.\n")
        except Exception as e:
            print(f"Error deleting task: {e}\n")

    def mark_task_completed(self):
        try:
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
                print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except FileNotFoundError:
            print("Task file not found.\n")
        except json.JSONDecodeError:
            print("Error reading task file: Invalid JSON format.\n")
        except Exception as e:
            print(f"Error marking task as completed: {e}\n")
    
    def mark_task_not_completed(self):
        try:
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
                print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except FileNotFoundError:
            print("Task file not found.\n")
        except json.JSONDecodeError:
            print("Error reading task file: Invalid JSON format.\n")
        except Exception as e:
            print(f"Error marking task as not completed: {e}\n")