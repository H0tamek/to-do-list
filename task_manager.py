# Class for working with tasks

import sqlite3

from database import TaskDatabase

class TaskManager:
    def __init__(self):
        self.database = TaskDatabase()
        
    def view_tasks(self):
        try:
            tasks = self.database.get_all_tasks()
            if not tasks:
                print("Task list is empty.\n")
                return

            for task in tasks:
                print(f"ID: {task['id']}, Text: {task['text']}, Status: {task['status']}")
            print()
        except sqlite3.Error as e:
            print(f"Database error while viewing tasks: {e}\n")
        except Exception as e:
            print(f"Error viewing tasks: {e}\n")
    
    def add_task(self):
        try:
            text = input("Enter task text: ")
            cleaned_text = text.strip()

            if not cleaned_text:
                print("Task text cannot be empty.\n")
                return

            task_id = self.database.add_task(cleaned_text)
            print(f"Task successfully added with ID {task_id}.\n")
        except sqlite3.Error as e:
            print(f"Database error while adding task: {e}\n")
        except Exception as e:
            print(f"Error adding task: {e}\n")
    
    def edit_task(self):
        try:
            task_id = int(input("Enter the ID of the task you want to edit: "))
            new_text = input("Enter new task text: ").strip()

            if not new_text:
                print("Task text cannot be empty.\n")
                return

            if self.database.update_task(task_id, new_text):
                print("Task successfully modified.\n")
                return

            print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while editing task: {e}\n")
        except Exception as e:
            print(f"Error editing task: {e}\n")
    
    def delete_task(self):
        try:
            task_id = int(input("Enter the ID of the task you want to delete: "))

            if self.database.delete_task(task_id):
                print("Task successfully deleted.\n")
                return

            print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while deleting task: {e}\n")
        except Exception as e:
            print(f"Error deleting task: {e}\n")

    def mark_task_completed(self):
        try:
            task_id = int(input("Enter the ID of the task you want to mark as completed: "))

            if self.database.update_status(task_id, 'Completed'):
                print("Task successfully marked as completed.\n")
                return

            print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while updating task status: {e}\n")
        except Exception as e:
            print(f"Error marking task as completed: {e}\n")
    
    def mark_task_not_completed(self):
        try:
            task_id = int(input("Enter the ID of the task you want to mark as not completed: "))

            if self.database.update_status(task_id, 'Not Completed'):
                print("Task successfully marked as not completed.\n")
                return

            print("Task with specified ID not found.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while updating task status: {e}\n")
        except Exception as e:
            print(f"Error marking task as not completed: {e}\n")
