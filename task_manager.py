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
    
    def add_task(self, text):
        with open('task.json', 'r', encoding="utf-8") as file:
            tasks = json.load(file)
            task_id = len(tasks) + 1
            tasks.append({'id': task_id, 'text': text, 'status': 'В процессе'})
        with open('task.json', 'w', encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
    
    def edit_task(self):
        pass
    
    def delete_task(self):
        pass
    
    def mark_task_completed(self):
        pass
    
    def mark_task_not_completed(self):
        pass