import calendar
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from task_manager import TaskManager


class TodoApp:
    BG = "#23211f"
    PANEL = "#2c2825"
    PANEL_ALT = "#312c29"
    PANEL_SOFT = "#282522"
    TEXT = "#ead0ae"
    MUTED = "#b69d80"
    SUBTLE = "#8f7f6c"
    ACCENT = "#8ecf8b"
    ACCENT_SOFT = "#3b4a3d"
    BORDER = "#3b3531"
    CHIP = "#343c52"
    CHIP_TEXT = "#c8d7ff"
    DANGER = "#b86f67"

    def __init__(self):
        self.manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Todo Manager")
        self.root.geometry("1380x820")
        self.root.minsize(1200, 720)
        self.root.configure(bg=self.BG)

        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_task_id = None
        self.task_rows = {}

        self.text_var = tk.StringVar()
        self.category_var = tk.StringVar(value="General")
        self.tags_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.status_var = tk.StringVar(value="In Progress")
        self.summary_var = tk.StringVar()

        self._build_styles()
        self._build_layout()
        self._load_tasks()

    def _build_styles(self):
        self.root.option_add("*Entry.Background", self.PANEL_ALT)
        self.root.option_add("*Entry.Foreground", self.TEXT)
        self.root.option_add("*Entry.InsertBackground", self.TEXT)
        self.root.option_add("*Text.Background", self.PANEL_ALT)
        self.root.option_add("*Text.Foreground", self.TEXT)
        self.root.option_add("*Text.InsertBackground", self.TEXT)

    def _build_layout(self):
        shell = tk.Frame(self.root, bg=self.BG, padx=22, pady=18)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=0, minsize=280)
        shell.columnconfigure(1, weight=1)
        shell.columnconfigure(2, weight=0, minsize=300)
        shell.rowconfigure(0, weight=1)

        self._build_sidebar(shell)
        self._build_main_content(shell)
        self._build_calendar_panel(shell)

    def _panel(self, parent, padding=18, bg=None):
        frame = tk.Frame(
            parent,
            bg=bg or self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=padding,
            pady=padding,
        )
        return frame

    def _build_sidebar(self, parent):
        sidebar = self._panel(parent, padding=16, bg=self.PANEL_SOFT)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(2, weight=1)

        tk.Label(
            sidebar,
            text="Workspace",
            bg=self.PANEL_SOFT,
            fg=self.SUBTLE,
            font=("Segoe UI", 10),
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            sidebar,
            text="Projects",
            bg=self.PANEL_SOFT,
            fg=self.TEXT,
            font=("Georgia", 24, "bold"),
        ).grid(row=1, column=0, sticky="w", pady=(6, 18))

        list_shell = tk.Frame(sidebar, bg=self.PANEL_SOFT)
        list_shell.grid(row=2, column=0, sticky="nsew")
        list_shell.columnconfigure(0, weight=1)
        list_shell.rowconfigure(1, weight=1)

        tk.Label(
            list_shell,
            text="Task Library",
            bg=self.PANEL_SOFT,
            fg=self.MUTED,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.task_listbox = tk.Listbox(
            list_shell,
            bg=self.PANEL_ALT,
            fg=self.TEXT,
            selectbackground="#4b433d",
            selectforeground=self.TEXT,
            highlightthickness=0,
            borderwidth=0,
            activestyle="none",
            font=("Segoe UI", 10),
        )
        self.task_listbox.grid(row=1, column=0, sticky="nsew")
        self.task_listbox.bind("<<ListboxSelect>>", self._on_listbox_select)

        tk.Label(
            sidebar,
            textvariable=self.summary_var,
            bg=self.PANEL_SOFT,
            fg=self.SUBTLE,
            justify="left",
            wraplength=220,
        ).grid(row=3, column=0, sticky="ew", pady=(18, 0))

    def _build_main_content(self, parent):
        main = tk.Frame(parent, bg=self.BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        breadcrumb = tk.Frame(main, bg=self.BG)
        breadcrumb.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        breadcrumb.columnconfigure(0, weight=1)

        tk.Label(
            breadcrumb,
            text="Daily / Task Notes",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10),
        ).grid(row=0, column=0, sticky="w")

        self.date_title = tk.Label(
            breadcrumb,
            text=self._format_display_date(datetime.now().strftime("%Y-%m-%d")),
            bg=self.BG,
            fg=self.TEXT,
            font=("Georgia", 14),
        )
        self.date_title.grid(row=0, column=1, sticky="e")

        card = self._panel(main, padding=28, bg=self.BG)
        card.grid(row=1, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)

        self.header_date = tk.Label(
            card,
            text=self._format_display_date(datetime.now().strftime("%Y-%m-%d")),
            bg=self.BG,
            fg=self.TEXT,
            font=("Georgia", 27, "bold"),
        )
        self.header_date.grid(row=0, column=0, sticky="w")

        self.chips_frame = tk.Frame(card, bg=self.BG)
        self.chips_frame.grid(row=1, column=0, sticky="w", pady=(12, 22))

        properties = tk.Frame(card, bg=self.BG)
        properties.grid(row=2, column=0, sticky="ew")
        properties.columnconfigure(1, weight=1)

        tk.Label(
            properties,
            text="Properties",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        self._field_label(properties, "Task").grid(row=1, column=0, sticky="nw", pady=6)
        self.task_text = tk.Text(
            properties,
            height=4,
            wrap="word",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=10,
            font=("Segoe UI", 11),
        )
        self.task_text.grid(row=1, column=1, sticky="ew", pady=6)

        self._field_label(properties, "Category").grid(
            row=2, column=0, sticky="w", pady=6
        )
        self.category_entry = self._entry(properties, self.category_var)
        self.category_entry.grid(row=2, column=1, sticky="ew", pady=6)

        self._field_label(properties, "Tags").grid(row=3, column=0, sticky="w", pady=6)
        self.tags_entry = self._entry(properties, self.tags_var)
        self.tags_entry.grid(row=3, column=1, sticky="ew", pady=6)

        self._field_label(properties, "Due date").grid(
            row=4, column=0, sticky="w", pady=6
        )
        self.due_date_entry = self._entry(properties, self.due_date_var)
        self.due_date_entry.grid(row=4, column=1, sticky="ew", pady=6)

        tk.Label(
            properties,
            text="Use YYYY-MM-DD. Leave empty if the task has no deadline.",
            bg=self.BG,
            fg=self.SUBTLE,
            anchor="w",
        ).grid(row=5, column=1, sticky="w", pady=(0, 10))

        self._field_label(properties, "Status").grid(
            row=6, column=0, sticky="w", pady=6
        )
        self.status_menu = tk.OptionMenu(
            properties,
            self.status_var,
            "In Progress",
            "Completed",
            "Not Completed",
        )
        self.status_menu.configure(
            bg=self.PANEL_ALT,
            fg=self.TEXT,
            activebackground="#403932",
            activeforeground=self.TEXT,
            highlightthickness=0,
            relief="flat",
            anchor="w",
        )
        self.status_menu["menu"].configure(
            bg=self.PANEL_ALT, fg=self.TEXT, activebackground="#403932"
        )
        self.status_menu.grid(row=6, column=1, sticky="w", pady=6)

        actions = tk.Frame(card, bg=self.BG)
        actions.grid(row=3, column=0, sticky="ew", pady=(28, 0))
        for index in range(3):
            actions.columnconfigure(index, weight=1)

        self._button(actions, "New Note", self._clear_form, self.PANEL_ALT).grid(
            row=0, column=0, sticky="ew", padx=(0, 8)
        )
        self._button(actions, "Save Task", self._save_task, self.ACCENT_SOFT).grid(
            row=0, column=1, sticky="ew", padx=8
        )
        self._button(actions, "Delete", self._delete_task, "#46312e").grid(
            row=0, column=2, sticky="ew", padx=(8, 0)
        )

    def _build_calendar_panel(self, parent):
        panel = self._panel(parent, padding=18, bg=self.PANEL)
        panel.grid(row=0, column=2, sticky="nsew")
        panel.columnconfigure(0, weight=1)

        nav = tk.Frame(panel, bg=self.PANEL)
        nav.grid(row=0, column=0, sticky="ew")
        nav.columnconfigure(1, weight=1)

        self._button(nav, "<", self._previous_month, self.PANEL_ALT, width=3).grid(
            row=0, column=0, sticky="w"
        )
        self.calendar_title = tk.Label(
            nav,
            text="",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Georgia", 20, "bold"),
        )
        self.calendar_title.grid(row=0, column=1)
        self._button(nav, ">", self._next_month, self.PANEL_ALT, width=3).grid(
            row=0, column=2, sticky="e"
        )

        self.calendar_grid = tk.Frame(panel, bg=self.PANEL)
        self.calendar_grid.grid(row=1, column=0, sticky="nsew", pady=(20, 0))
        self._render_calendar()

    def _field_label(self, parent, text):
        return tk.Label(
            parent,
            text=text,
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10),
        )

    def _entry(self, parent, variable):
        return tk.Entry(
            parent,
            textvariable=variable,
            bg=self.PANEL_ALT,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.MUTED,
            font=("Segoe UI", 11),
        )

    def _button(self, parent, text, command, bg, width=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=self.TEXT,
            activebackground="#4a433e",
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=10,
            width=width,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )

    def _format_display_date(self, due_date):
        if not due_date:
            return "No due date"
        try:
            return datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return due_date

    def _parse_tags(self):
        raw_tags = self.tags_var.get().strip()
        if not raw_tags:
            return []
        return [tag.strip() for tag in raw_tags.split(",") if tag.strip()]

    def _load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.task_rows = {}

        tasks = self.manager.list_tasks()
        for index, task in enumerate(tasks):
            due = task["due_date"] if task["due_date"] else "No date"
            label = f"{task['text']}  [{task['category']}]  {due}"
            self.task_listbox.insert(tk.END, label)
            self.task_rows[index] = task["id"]

        total_tasks = len(tasks)
        completed_tasks = len([task for task in tasks if task["status"] == "Completed"])
        dated_tasks = len([task for task in tasks if task["due_date"]])
        self.summary_var.set(
            f"Tasks: {total_tasks}\nCompleted: {completed_tasks}\nWith due date: {dated_tasks}"
        )

        if self.selected_task_id is not None:
            for index, task_id in self.task_rows.items():
                if task_id == self.selected_task_id:
                    self.task_listbox.selection_clear(0, tk.END)
                    self.task_listbox.selection_set(index)
                    self.task_listbox.activate(index)
                    break

    def _on_listbox_select(self, _event=None):
        selection = self.task_listbox.curselection()
        if not selection:
            return

        task_id = self.task_rows.get(selection[0])
        if task_id is None:
            return

        task = self.manager.get_task(task_id)
        if not task:
            return

        self.selected_task_id = task_id
        self.task_text.delete("1.0", tk.END)
        self.task_text.insert("1.0", task["text"])
        self.category_var.set(task["category"])
        self.tags_var.set(task["tags"])
        self.due_date_var.set(task["due_date"])
        self.status_var.set(task["status"])
        display_date = task["due_date"] or datetime.now().strftime("%Y-%m-%d")
        self.header_date.config(text=self._format_display_date(display_date))
        self.date_title.config(text=self._format_display_date(display_date))
        self._render_tag_chips(task)

    def _render_tag_chips(self, task):
        for child in self.chips_frame.winfo_children():
            child.destroy()

        chips = []
        if task["category"]:
            chips.append((task["category"], self.CHIP, self.CHIP_TEXT))
        for tag in [tag.strip() for tag in task["tags"].split(",") if tag.strip()]:
            chips.append((f"#{tag}", self.PANEL_ALT, self.MUTED))
        if task["due_date"]:
            chips.append((task["due_date"], self.ACCENT_SOFT, self.ACCENT))

        if not chips:
            chips.append(("No properties yet", self.PANEL_ALT, self.SUBTLE))

        for index, (text, bg, fg) in enumerate(chips):
            chip = tk.Label(
                self.chips_frame,
                text=text,
                bg=bg,
                fg=fg,
                padx=10,
                pady=4,
                font=("Segoe UI", 9, "bold"),
            )
            chip.grid(row=0, column=index, padx=(0, 8), sticky="w")

    def _clear_form(self):
        self.selected_task_id = None
        self.task_listbox.selection_clear(0, tk.END)
        self.task_text.delete("1.0", tk.END)
        self.category_var.set("General")
        self.tags_var.set("")
        self.due_date_var.set("")
        self.status_var.set("In Progress")
        today = datetime.now().strftime("%Y-%m-%d")
        self.header_date.config(text=today)
        self.date_title.config(text=today)
        self._render_tag_chips({"category": "", "tags": "", "due_date": ""})

    def _save_task(self):
        text = self.task_text.get("1.0", tk.END).strip()
        try:
            if self.selected_task_id is None:
                task_id = self.manager.create_task(
                    text,
                    self.category_var.get(),
                    self._parse_tags(),
                    self.due_date_var.get(),
                )
                self.selected_task_id = task_id
            else:
                self.manager.update_task_details(
                    self.selected_task_id,
                    text,
                    self.category_var.get(),
                    self._parse_tags(),
                    self.due_date_var.get(),
                )
                self.manager.change_task_status(self.selected_task_id, self.status_var.get())

            self._load_tasks()
            self._select_current_task()
            messagebox.showinfo("Saved", "Task saved successfully.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to save task: {error}")

    def _select_current_task(self):
        if self.selected_task_id is None:
            return
        for index, task_id in self.task_rows.items():
            if task_id == self.selected_task_id:
                self.task_listbox.selection_clear(0, tk.END)
                self.task_listbox.selection_set(index)
                self.task_listbox.activate(index)
                self._on_listbox_select()
                break

    def _delete_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning("No selection", "Select a task first.")
            return

        if not messagebox.askyesno(
            "Delete task", "Do you want to delete the selected task?"
        ):
            return

        try:
            self.manager.remove_task(self.selected_task_id)
            self._load_tasks()
            self._clear_form()
            messagebox.showinfo("Deleted", "Task deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to delete task: {error}")

    def _render_calendar(self):
        for child in self.calendar_grid.winfo_children():
            child.destroy()

        month_label = datetime(self.current_year, self.current_month, 1).strftime("%b. %Y")
        self.calendar_title.config(text=month_label)

        weekdays = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
        for column, weekday in enumerate(weekdays):
            tk.Label(
                self.calendar_grid,
                text=weekday,
                bg=self.PANEL,
                fg=self.SUBTLE,
                width=4,
                pady=6,
                font=("Segoe UI", 9, "bold"),
            ).grid(row=0, column=column, padx=2, pady=2)

        cal = calendar.Calendar(firstweekday=0)
        today = datetime.now().date()
        for row_index, week in enumerate(
            cal.monthdatescalendar(self.current_year, self.current_month), start=1
        ):
            for col_index, day in enumerate(week):
                is_current = day.month == self.current_month
                is_today = day == today
                bg = self.PANEL if is_current else self.PANEL_ALT
                fg = self.TEXT if is_current else self.SUBTLE
                if is_today:
                    bg = self.ACCENT
                    fg = "#1a2218"

                tk.Label(
                    self.calendar_grid,
                    text=str(day.day),
                    bg=bg,
                    fg=fg,
                    width=4,
                    height=2,
                    font=("Segoe UI", 10, "bold" if is_today else "normal"),
                ).grid(row=row_index, column=col_index, padx=2, pady=2)

    def _previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._render_calendar()

    def _next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._render_calendar()

    def run(self):
        self._clear_form()
        self.root.mainloop()
