# Todo Manager

Todo Manager is a console-based task management application written in Python. It provides a straightforward workflow for creating, updating, tracking, and deleting tasks while keeping data stored locally in a SQLite database.

The application is designed to be lightweight, reliable, and easy to run in any standard Python environment without external dependencies.

## Overview

This project offers a simple command-line interface for day-to-day task tracking. It supports the full task lifecycle, from initial creation to completion, and includes persistent local storage with automatic migration from the legacy JSON format.

## Features

- View all tasks with their current status
- Add new tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as completed
- Mark tasks as not completed
- Organize tasks by category
- Add tags for filtering and grouping
- Store data in a local SQLite database
- Automatically migrate legacy data from `task.json` to `tasks.db`

## Task Statuses

- **In Progress**: The task is currently active
- **Completed**: The task has been finished
- **Not Completed**: The task could not be completed

## Requirements

- Python 3.6 or higher
- No third-party libraries required

## Installation

1. Clone the repository:

```bash
git clone https://github.com/H0tamek/to-do-list.git
cd to-do-list
```

2. Run the application:

```bash
python main.py
```

## Project Structure

```text
to-do-list/
|-- main.py
|-- task_manager.py
|-- database.py
|-- task.json
|-- tasks.db
`-- README.md
```

## Usage

After launching the application, the following menu is displayed:

```text
Choose action:
1. View task list
2. Add task
3. Edit task
4. Delete task
5. Mark task as completed
6. Mark which task could not be completed
7. Exit
```

### Typical Workflow

**Add a task**

- Select option `2`
- Enter the task description
- Enter a category or keep the default `General`
- Enter optional comma-separated tags
- The task is saved with the status `In Progress`

**View tasks**

```text
ID: 1, Text: Prepare release notes, Category: Work, Tags: release, docs, Status: In Progress
ID: 2, Text: Review deployment checklist, Category: Operations, Tags: deploy, Status: Completed
ID: 3, Text: Refactor reporting module, Category: Engineering, Tags: backend, cleanup, Status: Not Completed
```

**Edit a task**

- Select option `3`
- Enter the task ID
- Enter the updated task text
- Update the category and tags if needed
- The task status is reset to `In Progress`

**Delete a task**

- Select option `4`
- Enter the task ID
- The task is removed from storage

## Data Storage

The application stores active data in `tasks.db`, a local SQLite database created automatically on first run.

If a legacy `task.json` file is present and the database is empty, the application imports the existing tasks automatically. This allows older project versions to move to the database-backed version without losing data.

The previous JSON format looked like this:

```json
[
    {
        "id": 1,
        "text": "Learn Python basics",
        "status": "In Progress"
    },
    {
        "id": 2,
        "text": "Build first project",
        "status": "Completed"
    }
]
```

## Technical Details

- **Language:** Python 3
- **Storage Engine:** SQLite
- **Database File:** `tasks.db`
- **Architecture:** Class-based application structure
- **Persistence:** Automatic local storage for all task changes
- **ID Strategy:** Auto-incrementing task identifiers
- **Migration:** One-time import from `task.json` when applicable
- **Validation:** Basic input validation for menu actions and task IDs
- **Error Handling:** Graceful handling of invalid input and storage-related exceptions

## Future Enhancements

- [x] Add task categories/tags
- [ ] Implement due dates
- [ ] Add task priority levels
- [ ] Export to different formats
- [ ] Task history/audit trail
- [ ] Bulk operations (mark multiple tasks)

## Contributing

Contributions are welcome. If you would like to improve the project:

1. Fork the repository
2. Create a feature branch
3. Make and test your changes
4. Open a pull request

## License

This project is licensed under the [MIT License](LICENSE).

## Code Overview

### `main.py`

Application entry point. Displays the menu, reads user input, and delegates actions to the task manager.

### `task_manager.py`

Contains the `TaskManager` class and the main business logic for task operations, including task creation, editing, deletion, status updates, validation, and user-facing error handling.

### `database.py`

Provides the SQLite storage layer, database initialization, and migration logic from the legacy JSON format.

### `tasks.db`

Primary local database file used for persistent task storage.

### `task.json`

Legacy storage file kept for backward compatibility and automatic one-time migration.
