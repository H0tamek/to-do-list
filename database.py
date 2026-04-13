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
                    category TEXT NOT NULL DEFAULT 'General',
                    tags TEXT NOT NULL DEFAULT '',
                    due_date TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL CHECK (
                        status IN ('In Progress', 'Completed', 'Not Completed')
                    ),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            self._ensure_schema(connection)
            connection.commit()

    def _ensure_schema(self, connection):
        columns = {
            row[1] for row in connection.execute("PRAGMA table_info(tasks)").fetchall()
        }

        if "category" not in columns:
            connection.execute(
                "ALTER TABLE tasks ADD COLUMN category TEXT NOT NULL DEFAULT 'General'"
            )

        if "tags" not in columns:
            connection.execute(
                "ALTER TABLE tasks ADD COLUMN tags TEXT NOT NULL DEFAULT ''"
            )

        if "due_date" not in columns:
            connection.execute(
                "ALTER TABLE tasks ADD COLUMN due_date TEXT NOT NULL DEFAULT ''"
            )

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
                task_category = str(task.get("category", "General")).strip() or "General"
                task_tags = self._normalize_tags(task.get("tags", []))
                task_due_date = str(task.get("due_date", "")).strip()

                if not task_text:
                    continue

                if task_status not in {"In Progress", "Completed", "Not Completed"}:
                    task_status = "In Progress"

                valid_tasks.append(
                    (task_text, task_category, task_tags, task_due_date, task_status)
                )

            if valid_tasks:
                connection.executemany(
                    """
                    INSERT INTO tasks (text, category, tags, due_date, status, updated_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """,
                    valid_tasks,
                )
                connection.commit()

    def _normalize_tags(self, raw_tags):
        if isinstance(raw_tags, str):
            values = raw_tags.split(",")
        elif isinstance(raw_tags, list):
            values = raw_tags
        else:
            values = []

        normalized_tags = []
        for value in values:
            cleaned_value = str(value).strip()
            if cleaned_value and cleaned_value not in normalized_tags:
                normalized_tags.append(cleaned_value)

        return ", ".join(normalized_tags)

    def get_all_tasks(self):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT id, text, category, tags, due_date, status
                FROM tasks
                ORDER BY id
                """
            )
            return [
                {
                    "id": row[0],
                    "text": row[1],
                    "category": row[2],
                    "tags": row[3],
                    "due_date": row[4],
                    "status": row[5],
                }
                for row in cursor.fetchall()
            ]

    def get_task_by_id(self, task_id):
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, text, category, tags, due_date, status
                FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            ).fetchone()

            if not row:
                return None

            return {
                "id": row[0],
                "text": row[1],
                "category": row[2],
                "tags": row[3],
                "due_date": row[4],
                "status": row[5],
            }

    def add_task(self, text, category, tags, due_date):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (text, category, tags, due_date, status, updated_at)
                VALUES (?, ?, ?, ?, 'In Progress', CURRENT_TIMESTAMP)
                """,
                (text, category, self._normalize_tags(tags), due_date),
            )
            connection.commit()
            return cursor.lastrowid

    def update_task(self, task_id, new_text, category, tags, due_date):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET text = ?, category = ?, tags = ?, due_date = ?,
                    status = 'In Progress', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (new_text, category, self._normalize_tags(tags), due_date, task_id),
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
