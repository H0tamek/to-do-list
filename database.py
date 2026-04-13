import json
import sqlite3
from pathlib import Path


class TaskDatabase:
    def __init__(self, db_path="tasks.db", legacy_json_path="task.json"):
        self.db_path = Path(db_path)
        self.legacy_json_path = Path(legacy_json_path)
        self._initialize_database()
        self._migrate_legacy_json()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize_database(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (
                        status IN ('In Progress', 'Completed', 'Not Completed')
                    ),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()

    def _migrate_legacy_json(self):
        if not self.legacy_json_path.exists():
            return

        with self._connect() as connection:
            existing_tasks = connection.execute(
                "SELECT COUNT(*) FROM tasks"
            ).fetchone()[0]

            if existing_tasks > 0:
                return

            try:
                with self.legacy_json_path.open("r", encoding="utf-8") as file:
                    tasks = json.load(file)
            except (json.JSONDecodeError, OSError):
                return

            valid_tasks = []
            for task in tasks:
                if not isinstance(task, dict):
                    continue

                task_text = str(task.get("text", "")).strip()
                task_status = str(task.get("status", "In Progress")).strip()

                if not task_text:
                    continue

                if task_status not in {"In Progress", "Completed", "Not Completed"}:
                    task_status = "In Progress"

                valid_tasks.append((task_text, task_status))

            if valid_tasks:
                connection.executemany(
                    """
                    INSERT INTO tasks (text, status, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    """,
                    valid_tasks,
                )
                connection.commit()

    def get_all_tasks(self):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT id, text, status
                FROM tasks
                ORDER BY id
                """
            )
            return [
                {"id": row[0], "text": row[1], "status": row[2]}
                for row in cursor.fetchall()
            ]

    def add_task(self, text):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (text, status, updated_at)
                VALUES (?, 'In Progress', CURRENT_TIMESTAMP)
                """,
                (text,),
            )
            connection.commit()
            return cursor.lastrowid

    def update_task(self, task_id, new_text):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET text = ?, status = 'In Progress', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (new_text, task_id),
            )
            connection.commit()
            return cursor.rowcount > 0

    def delete_task(self, task_id):
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,),
            )
            connection.commit()
            return cursor.rowcount > 0

    def update_status(self, task_id, status):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (status, task_id),
            )
            connection.commit()
            return cursor.rowcount > 0
