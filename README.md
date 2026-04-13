# Todo Manager

Todo Manager is a desktop note-taking application written in Python. It provides a focused workspace for writing notes, organizing them with categories and tags, tracking lightweight status, and storing everything locally in SQLite.

The application is local-first and now fully uses `PySide6` for a smoother and more modern desktop interface.

## Overview

This project has grown from a simple task tracker into a note workspace for day-to-day planning, writing, and lightweight organization. It keeps the local SQLite storage model and still supports one-time import from legacy JSON files when they are present.

The current version uses a Qt-based desktop interface built with `PySide6`, following a dark note-workspace layout with a left note library, a central editor, and a right calendar panel that can be hidden when not needed.

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
- Pin important notes to the top of the library
- Filter notes by pinned state, completion, or upcoming due dates
- Auto-save changes while writing
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
|-- tasks.db
|-- requirements.txt
`-- README.md
```

## Usage

After launching the application, the Qt desktop interface opens directly.

### Typical Workflow

**Add a note**

- Create or select a note in the left note list
- Enter the title and content in the main editor
- Enter a category or keep the default `General`
- Enter optional comma-separated tags
- Add a due date in `YYYY-MM-DD` format if needed
- Save the note or let auto-save handle it

**View notes**

- Browse notes from the left sidebar
- Review and edit note details in the center panel
- Use the calendar panel on the right for quick date context
- Hide the calendar panel when you want a cleaner writing layout
- Pin important notes to keep them at the top
- Use the quick filters to focus on pinned, completed, or upcoming notes

**Edit a note**

- Select a note from the left sidebar
- Update its content, category, tags, due date, or status
- Save the note to persist the changes, or continue writing and let auto-save update it

**Delete a note**

- Select the note
- Click `Delete`
- Confirm the action

## Data Storage

The application stores active data in `tasks.db`, a local SQLite database created automatically on first run.

If a legacy `task.json` file is present locally and the database is empty, the application imports the existing notes automatically. This allows older project versions to move to the database-backed version without losing data.

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
- **Architecture:** SQLite-backed note layer with a PySide6 desktop client
- **Persistence:** Automatic local storage for all task changes
- **ID Strategy:** Auto-incrementing task identifiers
- **Migration:** One-time import from `task.json` when applicable
- **Due Dates:** Stored in `YYYY-MM-DD` format
- **Pinning:** Important notes can be pinned to the top of the library
- **Auto-save:** Ongoing changes are saved automatically while writing
- **Validation:** Basic input validation for task data and due dates
- **Error Handling:** Graceful handling of invalid input and storage-related exceptions

## Future Enhancements

- [x] Add task categories/tags
- [x] Implement due dates
- [x] Migrate the desktop interface to PySide6
- [x] Add pinned notes and quick filters
- [x] Add hideable calendar panel
- [ ] Add markdown formatting and preview mode
- [ ] Add note folders or collections
- [ ] Add attachments and image support
- [ ] Add note history and restore points
- [ ] Add export and backup workflows

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

Qt desktop user interface built with `PySide6`. Provides the dark workspace, note list, quick filters, pinning, auto-save, due dates, search, and a hideable calendar panel.

### `task_manager.py`

Contains the `TaskManager` class and the main business logic for task operations, including task creation, editing, deletion, status updates, validation, and user-facing error handling.

### `database.py`

Provides the SQLite storage layer, database initialization, and migration logic from the legacy JSON format.

### `tasks.db`

Primary local database file used for persistent task storage.

Legacy `task.json` files can still be imported if they are present locally, but they are no longer part of the main project structure.
