import tkinter as tk
from tkinter import messagebox, ttk

from task_manager import TaskManager


class TodoApp:
    def __init__(self):
        self.manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Todo Manager")
        self.root.geometry("980x620")
        self.root.minsize(860, 520)
        self.selected_task_id = None

        self.text_var = tk.StringVar()
        self.category_var = tk.StringVar(value="General")
        self.tags_var = tk.StringVar()
        self.status_var = tk.StringVar(value="In Progress")

        self._build_layout()
        self._load_tasks()

    def _build_layout(self):
        self.root.configure(bg="#f4f6f8")

        header = tk.Frame(self.root, bg="#1f2937", padx=24, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Todo Manager",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#1f2937",
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Manage tasks, categories, tags, and status from a single workspace.",
            font=("Segoe UI", 10),
            fg="#d1d5db",
            bg="#1f2937",
        ).pack(anchor="w", pady=(4, 0))

        content = tk.Frame(self.root, bg="#f4f6f8", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        self._build_task_table(content)
        self._build_editor_panel(content)

    def _build_task_table(self, parent):
        table_card = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=14, pady=14)
        table_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        table_card.rowconfigure(1, weight=1)
        table_card.columnconfigure(0, weight=1)

        title_row = tk.Frame(table_card, bg="white")
        title_row.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        title_row.columnconfigure(0, weight=1)

        tk.Label(
            title_row,
            text="Tasks",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#111827",
        ).grid(row=0, column=0, sticky="w")

        ttk.Button(title_row, text="Refresh", command=self._load_tasks).grid(
            row=0, column=1, sticky="e"
        )

        columns = ("id", "text", "category", "tags", "status")
        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self._on_task_select)

        headings = {
            "id": "ID",
            "text": "Task",
            "category": "Category",
            "tags": "Tags",
            "status": "Status",
        }
        widths = {"id": 55, "text": 280, "category": 140, "tags": 190, "status": 120}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="w")

        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

    def _build_editor_panel(self, parent):
        editor = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=18, pady=18)
        editor.grid(row=0, column=1, sticky="nsew")
        editor.columnconfigure(0, weight=1)

        tk.Label(
            editor,
            text="Task Details",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#111827",
        ).grid(row=0, column=0, sticky="w")

        tk.Label(editor, text="Task text", bg="white", anchor="w").grid(
            row=1, column=0, sticky="ew", pady=(18, 6)
        )
        ttk.Entry(editor, textvariable=self.text_var).grid(row=2, column=0, sticky="ew")

        tk.Label(editor, text="Category", bg="white", anchor="w").grid(
            row=3, column=0, sticky="ew", pady=(14, 6)
        )
        ttk.Entry(editor, textvariable=self.category_var).grid(
            row=4, column=0, sticky="ew"
        )

        tk.Label(editor, text="Tags", bg="white", anchor="w").grid(
            row=5, column=0, sticky="ew", pady=(14, 6)
        )
        ttk.Entry(editor, textvariable=self.tags_var).grid(row=6, column=0, sticky="ew")

        tk.Label(
            editor,
            text="Use commas to separate tags, for example: work, urgent, backend",
            bg="white",
            fg="#6b7280",
            anchor="w",
            justify="left",
        ).grid(row=7, column=0, sticky="ew", pady=(6, 16))

        tk.Label(editor, text="Status", bg="white", anchor="w").grid(
            row=8, column=0, sticky="ew", pady=(0, 6)
        )
        status_combo = ttk.Combobox(
            editor,
            textvariable=self.status_var,
            values=("In Progress", "Completed", "Not Completed"),
            state="readonly",
        )
        status_combo.grid(row=9, column=0, sticky="ew")

        actions = tk.Frame(editor, bg="white")
        actions.grid(row=10, column=0, sticky="ew", pady=(20, 10))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)

        ttk.Button(actions, text="Add Task", command=self._add_task).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(actions, text="Update Task", command=self._update_task).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )
        ttk.Button(actions, text="Delete Task", command=self._delete_task).grid(
            row=1, column=0, sticky="ew", padx=(0, 6), pady=(10, 0)
        )
        ttk.Button(actions, text="Clear Form", command=self._clear_form).grid(
            row=1, column=1, sticky="ew", padx=(6, 0), pady=(10, 0)
        )

        status_actions = tk.Frame(editor, bg="white")
        status_actions.grid(row=11, column=0, sticky="ew", pady=(10, 0))
        status_actions.columnconfigure(0, weight=1)
        status_actions.columnconfigure(1, weight=1)

        ttk.Button(
            status_actions,
            text="Set Completed",
            command=lambda: self._set_status("Completed"),
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(
            status_actions,
            text="Set Not Completed",
            command=lambda: self._set_status("Not Completed"),
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def _parse_tags(self):
        raw_tags = self.tags_var.get().strip()
        if not raw_tags:
            return []
        return [tag.strip() for tag in raw_tags.split(",") if tag.strip()]

    def _load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for task in self.manager.list_tasks():
            self.tree.insert(
                "",
                "end",
                iid=str(task["id"]),
                values=(
                    task["id"],
                    task["text"],
                    task["category"],
                    task["tags"] or "No tags",
                    task["status"],
                ),
            )

    def _on_task_select(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return

        task_id = int(selection[0])
        task = self.manager.get_task(task_id)
        if not task:
            return

        self.selected_task_id = task_id
        self.text_var.set(task["text"])
        self.category_var.set(task["category"])
        self.tags_var.set(task["tags"])
        self.status_var.set(task["status"])

    def _clear_form(self):
        self.selected_task_id = None
        self.text_var.set("")
        self.category_var.set("General")
        self.tags_var.set("")
        self.status_var.set("In Progress")
        self.tree.selection_remove(*self.tree.selection())

    def _add_task(self):
        try:
            task_id = self.manager.create_task(
                self.text_var.get(), self.category_var.get(), self._parse_tags()
            )
            self._load_tasks()
            self.tree.selection_set(str(task_id))
            self.tree.focus(str(task_id))
            self._on_task_select()
            messagebox.showinfo("Success", f"Task {task_id} was added successfully.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to add task: {error}")

    def _update_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning("No task selected", "Select a task to update it.")
            return

        try:
            self.manager.update_task_details(
                self.selected_task_id,
                self.text_var.get(),
                self.category_var.get(),
                self._parse_tags(),
            )
            self.manager.change_task_status(self.selected_task_id, self.status_var.get())
            self._load_tasks()
            self.tree.selection_set(str(self.selected_task_id))
            self.tree.focus(str(self.selected_task_id))
            self._on_task_select()
            messagebox.showinfo("Success", "Task updated successfully.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to update task: {error}")

    def _delete_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning("No task selected", "Select a task to delete it.")
            return

        if not messagebox.askyesno(
            "Delete task", "Are you sure you want to delete the selected task?"
        ):
            return

        try:
            self.manager.remove_task(self.selected_task_id)
            self._load_tasks()
            self._clear_form()
            messagebox.showinfo("Success", "Task deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to delete task: {error}")

    def _set_status(self, status):
        if self.selected_task_id is None:
            messagebox.showwarning("No task selected", "Select a task first.")
            return

        try:
            self.manager.change_task_status(self.selected_task_id, status)
            self.status_var.set(status)
            self._load_tasks()
            self.tree.selection_set(str(self.selected_task_id))
            self.tree.focus(str(self.selected_task_id))
            self._on_task_select()
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to update status: {error}")

    def run(self):
        self.root.mainloop()
