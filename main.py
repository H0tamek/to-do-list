# Program launch file

import task_manager

if __name__ == "__main__":
    
    tasks_manager = task_manager.TaskManager()
    
    while True:
        print("Choose action:")
        print("1. View task list")
        print("2. Add task")
        print("3. Edit task")
        print("4. Delete task")
        print("5. Mark task as completed")
        print("6. Mark which task could not be completed")
        print("7. Exit")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            # View task list
            tasks_manager.view_tasks()
            
        elif choice == "2":
            # Add task
            tasks_manager.add_task()
            
        elif choice == "3":
            # Edit task
            tasks_manager.edit_task()
            
        elif choice == "4":
            # Delete task
            tasks_manager.delete_task()
            
        elif choice == "5":
            # Mark task as completed
            tasks_manager.mark_task_completed()
        
        elif choice == "6":
            # Mark which task could not be completed
            tasks_manager.mark_task_not_completed()
            
        elif choice == "7":
            # Exit
            break