# Class for working with tasks

from datetime import datetime
import sqlite3

from database import TaskDatabase

class TaskManager:
    def __init__(self):
        self.database = TaskDatabase()

    def _normalize_title(self, title, content):
        cleaned_title = title.strip()
        if cleaned_title:
            return cleaned_title

        first_line = content.strip().splitlines()[0] if content.strip() else ""
        return first_line[:60] if first_line else "Untitled note"

    def _normalize_due_date(self, due_date):
        cleaned_due_date = due_date.strip()
        if not cleaned_due_date:
            return ""

        datetime.strptime(cleaned_due_date, "%Y-%m-%d")
        return cleaned_due_date

    def list_tasks(self):
        return self.database.get_all_tasks()

    def create_task(
        self, title, text, category="General", tags=None, due_date="", pinned=False
    ):
        cleaned_text = text.strip()
        cleaned_category = category.strip() or "General"
        normalized_title = self._normalize_title(title, cleaned_text)

        if not cleaned_text and not normalized_title.strip():
            raise ValueError("Add a title or note content before saving.")

        normalized_due_date = self._normalize_due_date(due_date)
        return self.database.add_task(
            normalized_title,
            cleaned_text,
            cleaned_category,
            tags or [],
            normalized_due_date,
            pinned,
        )

    def get_task(self, task_id):
        return self.database.get_task_by_id(task_id)

    def update_task_details(
        self, task_id, title, text, category, tags, due_date="", pinned=False
    ):
        cleaned_text = text.strip()
        cleaned_category = category.strip() or "General"
        normalized_title = self._normalize_title(title, cleaned_text)

        if not cleaned_text and not normalized_title.strip():
            raise ValueError("Add a title or note content before saving.")

        normalized_due_date = self._normalize_due_date(due_date)
        updated = self.database.update_task(
            task_id,
            normalized_title,
            cleaned_text,
            cleaned_category,
            tags or [],
            normalized_due_date,
            pinned,
        )
        if not updated:
            raise ValueError("Note with specified ID not found.")

    def remove_task(self, task_id):
        deleted = self.database.delete_task(task_id)
        if not deleted:
            raise ValueError("Note with specified ID not found.")

    def change_task_status(self, task_id, status):
        updated = self.database.update_status(task_id, status)
        if not updated:
            raise ValueError("Note with specified ID not found.")

    def toggle_pinned(self, task_id, pinned):
        updated = self.database.update_pinned(task_id, pinned)
        if not updated:
            raise ValueError("Note with specified ID not found.")

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

    def _prompt_due_date(self):
        due_date = input("Enter due date in YYYY-MM-DD format (optional): ").strip()
        if not due_date:
            return ""
        return self._normalize_due_date(due_date)

    def _prompt_tags_for_edit(self, current_tags):
        prompt_suffix = current_tags if current_tags else "no tags"
        tags = input(
            f"Enter task tags separated by commas (leave empty to keep {prompt_suffix}): "
        ).strip()
        if not tags:
            return current_tags
        return [tag.strip() for tag in tags.split(",") if tag.strip()]

    def _prompt_due_date_for_edit(self, current_due_date):
        due_date_hint = current_due_date or "no due date"
        due_date = input(
            f"Enter due date in YYYY-MM-DD format (leave empty to keep {due_date_hint}): "
        ).strip()
        if not due_date:
            return current_due_date
        return self._normalize_due_date(due_date)
        
    def view_tasks(self):
        try:
            tasks = self.list_tasks()
            if not tasks:
                print("Task list is empty.\n")
                return

            for task in tasks:
                tags = task["tags"] if task["tags"] else "No tags"
                due_date = task["due_date"] if task["due_date"] else "No due date"
                print(
                    f"ID: {task['id']}, Title: {task['title']}, Text: {task['text']}, "
                    f"Category: {task['category']}, Tags: {tags}, "
                    f"Due Date: {due_date}, Status: {task['status']}"
                )
            print()
        except sqlite3.Error as e:
            print(f"Database error while viewing tasks: {e}\n")
        except Exception as e:
            print(f"Error viewing tasks: {e}\n")
    
    def add_task(self):
        try:
            title = input("Enter note title: ")
            text = input("Enter note text: ")
            cleaned_text = text.strip()

            if not cleaned_text:
                print("Note content cannot be empty.\n")
                return

            category = self._prompt_category()
            tags = self._prompt_tags()
            due_date = self._prompt_due_date()
            task_id = self.create_task(title, cleaned_text, category, tags, due_date)
            print(f"Note successfully added with ID {task_id}.\n")
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
                print("Note with specified ID not found.\n")
                return

            new_title = input("Enter new note title: ").strip()
            new_text = input("Enter new note text: ").strip()

            if not new_text:
                print("Note content cannot be empty.\n")
                return

            category = self._prompt_category_for_edit(existing_task["category"])
            tags = self._prompt_tags_for_edit(existing_task["tags"])
            due_date = self._prompt_due_date_for_edit(existing_task["due_date"])

            self.update_task_details(
                task_id, new_title, new_text, category, tags, due_date
            )
            print("Note successfully modified.\n")
        except ValueError as e:
            error_message = str(e)
            if "invalid literal for int()" in error_message:
                print("Invalid task ID format. Please enter a number.\n")
            else:
                print(f"{error_message}\n")
        except sqlite3.Error as e:
            print(f"Database error while editing task: {e}\n")
        except Exception as e:
            print(f"Error editing task: {e}\n")
    
    def delete_task(self):
        try:
            task_id = int(input("Enter the ID of the task you want to delete: "))
            self.remove_task(task_id)
            print("Note successfully deleted.\n")
        except ValueError as e:
            error_message = str(e)
            if "invalid literal for int()" in error_message:
                print("Invalid task ID format. Please enter a number.\n")
            else:
                print(f"{error_message}\n")
        except sqlite3.Error as e:
            print(f"Database error while deleting task: {e}\n")
        except Exception as e:
            print(f"Error deleting task: {e}\n")

    def mark_task_completed(self):
        try:
            task_id = int(input("Enter the ID of the task you want to mark as completed: "))
            self.change_task_status(task_id, "Completed")
            print("Task successfully marked as completed.\n")
        except ValueError as e:
            error_message = str(e)
            if "invalid literal for int()" in error_message:
                print("Invalid task ID format. Please enter a number.\n")
            else:
                print(f"{error_message}\n")
        except sqlite3.Error as e:
            print(f"Database error while updating task status: {e}\n")
        except Exception as e:
            print(f"Error marking task as completed: {e}\n")
    
    def mark_task_not_completed(self):
        try:
            task_id = int(input("Enter the ID of the task you want to mark as not completed: "))
            self.change_task_status(task_id, "Not Completed")
            print("Task successfully marked as not completed.\n")
        except ValueError as e:
            error_message = str(e)
            if "invalid literal for int()" in error_message:
                print("Invalid task ID format. Please enter a number.\n")
            else:
                print(f"{error_message}\n")
        except sqlite3.Error as e:
            print(f"Database error while updating task status: {e}\n")
        except Exception as e:
            print(f"Error marking task as not completed: {e}\n")
