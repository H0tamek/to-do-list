# Класс для роботы с задачами

import json
import os

class TaskManager:
    def __init__(self):
        # Убедимся, что файл существует
        if not os.path.exists('task.json'):
            with open('task.json', 'w', encoding='utf-8') as file:
                json.dump([], file)
        
    def view_tasks(self):
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            for task in tasks:
                print(f"ID: {task['id']}, Текст: {task['text']}, Статус: {task['status']}")
    
    def add_task(self):
        pass
    
    def edit_task(self):
        pass
    
    def delete_task(self):
        pass
    
    def mark_task_completed(self):
        pass
    
    def mark_task_not_completed(self):
        pass