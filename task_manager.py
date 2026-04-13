# Class for working with tasks

import sqlite3

from database import TaskDatabase

class TaskManager:
    def __init__(self):
        self.database = TaskDatabase()

    def list_tasks(self):
        return self.database.get_all_tasks()

    def create_task(self, text, category="General", tags=None):
        cleaned_text = text.strip()
        cleaned_category = category.strip() or "General"

        if not cleaned_text:
            raise ValueError("Task text cannot be empty.")

        return self.database.add_task(cleaned_text, cleaned_category, tags or [])

    def get_task(self, task_id):
        return self.database.get_task_by_id(task_id)

    def update_task_details(self, task_id, text, category, tags):
        cleaned_text = text.strip()
        cleaned_category = category.strip() or "General"

        if not cleaned_text:
            raise ValueError("Task text cannot be empty.")

        updated = self.database.update_task(
            task_id, cleaned_text, cleaned_category, tags or []
        )
        if not updated:
            raise ValueError("Task with specified ID not found.")

    def remove_task(self, task_id):
        deleted = self.database.delete_task(task_id)
        if not deleted:
            raise ValueError("Task with specified ID not found.")

    def change_task_status(self, task_id, status):
        updated = self.database.update_status(task_id, status)
        if not updated:
            raise ValueError("Task with specified ID not found.")

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
            tasks = self.list_tasks()
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
            task_id = self.create_task(cleaned_text, category, tags)
            print(f"Task successfully added with ID {task_id}.\n")
        except ValueError as e:
            print(f"{e}\n")
        except sqlite3.Error as e:
            print(f"Database error while adding task: {e}\n")
        except Exception as e:
            print(f"Error adding task: {e}\n")
    
    def edit_task(self):
        try:
            task_id = int(input("Enter the ID of the task you want to edit: "))
            existing_task = self.get_task(task_id)

            if not existing_task:
                print("Task with specified ID not found.\n")
                return

            new_text = input("Enter new task text: ").strip()

            if not new_text:
                print("Task text cannot be empty.\n")
                return

            category = self._prompt_category_for_edit(existing_task["category"])
            tags = self._prompt_tags_for_edit(existing_task["tags"])

            self.update_task_details(task_id, new_text, category, tags)
            print("Task successfully modified.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while editing task: {e}\n")
        except Exception as e:
            print(f"Error editing task: {e}\n")
    
    def delete_task(self):
        try:
            task_id = int(input("Enter the ID of the task you want to delete: "))
            self.remove_task(task_id)
            print("Task successfully deleted.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while deleting task: {e}\n")
        except Exception as e:
            print(f"Error deleting task: {e}\n")

    def mark_task_completed(self):
        try:
            task_id = int(input("Enter the ID of the task you want to mark as completed: "))
            self.change_task_status(task_id, "Completed")
            print("Task successfully marked as completed.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while updating task status: {e}\n")
        except Exception as e:
            print(f"Error marking task as completed: {e}\n")
    
    def mark_task_not_completed(self):
        try:
            task_id = int(input("Enter the ID of the task you want to mark as not completed: "))
            self.change_task_status(task_id, "Not Completed")
            print("Task successfully marked as not completed.\n")
        except ValueError:
            print("Invalid task ID format. Please enter a number.\n")
        except sqlite3.Error as e:
            print(f"Database error while updating task status: {e}\n")
        except Exception as e:
            print(f"Error marking task as not completed: {e}\n")
