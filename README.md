# Todo Manager

Todo Manager is gradually evolving into a desktop note-taking application written in Python. It provides a structured workspace for writing notes, organizing them with categories and tags, tracking status when needed, and storing everything locally in SQLite.

The application is designed to be local-first and reliable, and it is now beginning its migration from `tkinter` to `PySide6` to support a smoother and more modern desktop interface.

## Overview

This project offers a simple command-line interface for day-to-day task tracking. It supports the full task lifecycle, from initial creation to completion, and includes persistent local storage with automatic migration from the legacy JSON format.

The current version includes the first Qt-based desktop interface built with `PySide6`, following a dark note-workspace layout with a left note library, a central editor, and a right calendar panel that can be hidden when not needed.

## Features

- View all notes with their current status
- Add new notes
- Edit existing notes
- Delete notes
- Mark tasks as completed
- Mark tasks as not completed
- Organize tasks by category
- Add tags for filtering and grouping
- Assign due dates to tasks
- Search notes from the sidebar
- Toggle the right calendar panel on and off
- Store data in a local SQLite database
- Automatically migrate legacy data from `task.json` to `tasks.db`
- Manage tasks through a desktop graphical interface

## Task Statuses

- **In Progress**: The task is currently active
- **Completed**: The task has been finished
- **Not Completed**: The task could not be completed

## Requirements

- Python 3.10 or higher recommended
- `PySide6`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/H0tamek/to-do-list.git
cd to-do-list
```

2. Install dependencies:

```bash
python -m pip install PySide6
```

3. Run the application:

```bash
python main.py
```

This command opens the Qt desktop interface.

## Project Structure

```text
to-do-list/
|-- main.py
|-- qt_gui.py
|-- task_manager.py
|-- database.py
|-- task.json
|-- tasks.db
`-- README.md
```

## Usage

After launching the application, the Qt desktop interface opens directly.

### Typical Workflow

**Add a task**

- Create or select a note in the left task list
- Enter the task description in the main editor
- Enter a category or keep the default `General`
- Enter optional comma-separated tags
- Add a due date in `YYYY-MM-DD` format if needed
- Save the task

**View tasks**

- Browse notes from the left sidebar
- Review and edit note details in the center panel
- Use the calendar panel on the right for quick date context
- Hide the calendar panel when you want a cleaner writing layout

**Edit a task**

- Select a task from the left sidebar
- Update its content, category, tags, due date, or status
- Save the task to persist the changes

**Delete a task**

- Select the task
- Click `Delete`
- Confirm the action

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
- **Architecture:** SQLite-backed note layer with a Qt desktop client
- **Persistence:** Automatic local storage for all task changes
- **ID Strategy:** Auto-incrementing task identifiers
- **Migration:** One-time import from `task.json` when applicable
- **Due Dates:** Stored in `YYYY-MM-DD` format
- **Validation:** Basic input validation for task data and due dates
- **Error Handling:** Graceful handling of invalid input and storage-related exceptions

## Future Enhancements

- [x] Add task categories/tags
- [x] Implement due dates
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

Application entry point. Launches the Qt desktop interface.

### `qt_gui.py`

Qt desktop user interface built with `PySide6`. Provides the dark workspace, note list, note editor, due dates, search, and a hideable calendar panel.

### `gui.py`

Legacy `tkinter` interface kept temporarily while the migration to Qt is in progress.

### `task_manager.py`

Contains the `TaskManager` class and the main business logic for task operations, including task creation, editing, deletion, status updates, validation, and user-facing error handling.

### `database.py`

Provides the SQLite storage layer, database initialization, and migration logic from the legacy JSON format.

### `tasks.db`

Primary local database file used for persistent task storage.

### `task.json`

Legacy storage file kept for backward compatibility and automatic one-time migration.
