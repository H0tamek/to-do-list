# 📝 Todo Manager

A simple console-based task management application written in Python. Perfect for learning Python fundamentals and working with JSON files!

## 🚀 Features

- ✅ View all tasks with status indicators
- ➕ Add new tasks
- ✏️ Edit existing tasks
- 🗑️ Delete tasks
- ✔️ Mark tasks as completed
- ❌ Mark tasks as not completed
- 💾 Automatic JSON file storage

## 🎯 Task Statuses

- 🔄 **In Progress** - task is currently being worked on
- ✅ **Completed** - task has been successfully finished
- ❌ **Not Completed** - task could not be completed

## 📋 Requirements

- Python 3.6 or higher
- No additional libraries required!

## 🛠️ Installation and Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/H0tamek/to-do-list.git
   cd todo-manager
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
todo-manager/
├── main.py              # Main application entry point
├── task_manager.py      # TaskManager class with core functionality
├── task.json           # JSON file for storing tasks (auto-created)
└── README.md           # Project documentation
```

## 🎮 How to Use

After running the program, you'll see the main menu:

```
Choose action:
1. View task list
2. Add task
3. Edit task
4. Delete task
5. Mark task as completed
6. Mark which task could not be completed
7. Exit

Enter action number:
```

### Usage Examples

**Adding a task:**
- Select option 2
- Enter your task description
- Task is automatically saved with "In Progress" status

**Viewing tasks:**
```
ID: 1, Text: Learn Python basics, Status: In Progress
ID: 2, Text: Build first project, Status: Completed
ID: 3, Text: Solve complex algorithm, Status: Not Completed
```

**Editing a task:**
- Select option 3
- Enter the task ID you want to edit
- Enter new task text
- Status automatically resets to "In Progress"

**Deleting a task:**
- Select option 4
- Enter the task ID you want to delete
- Task is permanently removed

## 💾 Data Format

Tasks are stored in `task.json` file with the following structure:

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

## 🔧 Technical Details

- **Language:** Python 3
- **Data Storage:** JSON file (`task.json`)
- **Architecture:** Simple class-based structure
- **File Handling:** Automatic file creation and UTF-8 encoding
- **ID Management:** Auto-incrementing task IDs

## ✨ Key Features of Implementation

- **Automatic File Creation:** Creates `task.json` if it doesn't exist
- **UTF-8 Support:** Handles international characters properly
- **Simple Menu System:** Easy-to-use console interface
- **Error Handling:** Basic validation for user inputs
- **Persistent Storage:** All changes are immediately saved to file

## 🚀 Future Enhancements

- [ ] Add task categories/tags
- [ ] Implement due dates
- [ ] Add task priority levels
- [ ] Search functionality
- [ ] Export to different formats
- [ ] GUI interface
- [ ] Better error handling and validation

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes and test them
4. Create a Pull Request

## 📚 Learning Objectives

This project demonstrates:
- Basic Python programming concepts
- Working with JSON files
- Class-based programming
- File I/O operations
- Menu-driven applications
- Error handling basics

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Created as a learning project to practice Python fundamentals and file handling.

---

**Happy coding! 🎉**

## 🔍 Code Overview

### main.py
Contains the main application loop and menu system. Handles user input and delegates actions to the TaskManager class.

### task_manager.py
Core functionality including:
- `TaskManager` class with all task operations
- JSON file handling (read/write)
- Task CRUD operations (Create, Read, Update, Delete)
- Status management

### task.json
Auto-generated JSON file that stores all task data with proper UTF-8 encoding.