# Class for working with tasks

import sqlite3

from database import TaskDatabase

class TaskManager:
    def __init__(self):
        self.database = TaskDatabase()

    def _prompt_category(self):
        category = input("Enter task category (leave empty for General): ").strip()
        return category or "General"

    def _prompt_category_for_edit(self, current_category):
        category = input(
            f"Enter task category (leave empty to keep '{current_category}'): "
        ).strip()
        return category or current_category

    def _prompt_tags(self):
        tags = input("Enter task tags separated by commas (optional): ").strip()
        if not tags:
            return []
        return [tag.strip() for tag in tags.split(",") if tag.strip()]

    def _prompt_tags_for_edit(self, current_tags):
        prompt_suffix = current_tags if current_tags else "no tags"
        tags = input(
            f"Enter task tags separated by commas (leave empty to keep {prompt_suffix}): "
        ).strip()
        if not tags:
            return current_tags
        return [tag.strip() for tag in tags.split(",") if tag.strip()]
        
    def view_tasks(self):
        try:
            tasks = self.database.get_all_tasks()
            if not tasks:
                print("Task list is empty.\n")
                return

            for task in tasks:
                tags = task["tags"] if task["tags"] else "No tags"
                print(
                    f"ID: {task['id']}, Text: {task['text']}, "
                    f"Category: {task['category']}, Tags: {tags}, "
                    f"Status: {task['status']}"
                )
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

            category = self._prompt_category()
            tags = self._prompt_tags()
            task_id = self.database.add_task(cleaned_text, category, tags)
            print(f"Task successfully added with ID {task_id}.\n")
        except sqlite3.Error as e:
            print(f"Database error while adding task: {e}\n")
        except Exception as e:
            print(f"Error adding task: {e}\n")
    
    def edit_task(self):
        try:
            task_id = int(input("Enter the ID of the task you want to edit: "))
            existing_task = self.database.get_task_by_id(task_id)

            if not existing_task:
                print("Task with specified ID not found.\n")
                return

            new_text = input("Enter new task text: ").strip()

            if not new_text:
                print("Task text cannot be empty.\n")
                return

            category = self._prompt_category_for_edit(existing_task["category"])
            tags = self._prompt_tags_for_edit(existing_task["tags"])

            if self.database.update_task(task_id, new_text, category, tags):
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
