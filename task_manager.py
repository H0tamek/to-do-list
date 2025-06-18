# Класс для роботы с задачами

import json
import os

class TaskManager:
    def __init__(self):
        # Убедимся, что файл существует
        if not os.path.exists('task.json'):
            with open('task.json', 'w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False, indent=4)
        
    def view_tasks(self):
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            for task in tasks:
                print(f"ID: {task['id']}, Текст: {task['text']}, Статус: {task['status']}")
            print()
    
    def add_task(self):
        text = input("Введите текст задачи: ")
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = max([task['id'] for task in tasks], default=0) + 1
            tasks.append({'id': task_id, 'text': text, 'status': 'В процессе'})
        with open('task.json', 'w', encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
        print("Задача успешно добавлена.\n")
    
    def edit_task(self):
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Введите ID задачи, которую хотите изменить: "))
            for task in tasks:
                if task['id'] == task_id:
                    new_text = input("Введите новый текст задачи: ")
                    task['text'] = new_text
                    task['status'] = 'В процессе'
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Задача успешно изменена.\n")
                    return
    
    def delete_task(self):
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Введите ID задачи, которую хотите удалить: "))
            for task in tasks:
                if task['id'] == task_id:
                    tasks.remove(task)
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Задача успешно удалена.\n")
                    return

    def mark_task_completed(self):
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Введите ID задачи, которую хотите отметить выполненной: "))
            for task in tasks:
                if task['id'] == task_id:
                    task['status'] = 'Выполнено'
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Задача успешно отмечена выполненной.\n")
                    return
    
    def mark_task_not_completed(self):
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = int(input("Введите ID задачи, которую хотите отметить не выполненной: "))
            for task in tasks:
                if task['id'] == task_id:
                    task['status'] = 'Не выполнено'
                    with open('task.json', 'w', encoding="utf-8") as file:
                        json.dump(tasks, file, ensure_ascii=False, indent=4)
                    print("Задача успешно отмечена не выполненной.\n")
                    return