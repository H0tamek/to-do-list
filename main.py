# Файл запуска программы

import task_manager

if __name__ == "__main__":
    
    tasks_manager = task_manager.TaskManager()
    
    while True:
        print("Выберите действие:")
        print("1. Посмотреть список задач")
        print("2. Добавь задачу")
        print("3. Изменить задачу")
        print("4. Удалить задачу")
        print("5. Отметить задачу выполненной")
        print("6. Отметить какую задачу не смог выполнить")
        print("7. Выход")
        
        choice = input("Введите номер действия: ")
        
        if choice == "1":
            # Посмотреть список задач
            tasks_manager.view_tasks()
            
        elif choice == "2":
            # Добавить задачу
            tasks_manager.add_task()
            
        elif choice == "3":
            # Изменить задачу
            tasks_manager.edit_task()
            
        elif choice == "4":
            # Удалить задачу
            tasks_manager.delete_task()
            
        elif choice == "5":
            # Отметить задачу выполненной
            tasks_manager.mark_task_completed()
        
        elif choice == "6":
            # Отметить какую задачу не смог выполнить
            tasks_manager.mark_task_not_completed()
            
        elif choice == "7":
            # Выход
            break