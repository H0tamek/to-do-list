# Файл запуска программы

import task_manager

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
        pass
    elif choice == "3":
        # Изменить задачу
        pass
    elif choice == "4":
        # Удалить задачу
        pass
    elif choice == "5":
        # Отметить задачу выполненной
        pass
    elif choice == "6":
        # Отметить какую задачу не смог выполнить
        pass
    elif choice == "7":
        # Выход
        break