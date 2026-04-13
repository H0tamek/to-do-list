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

    def __init__(self):
        self.manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("Todo Manager")
        self.root.geometry("1450x860")
        self.root.minsize(1240, 760)
        self.root.configure(bg=self.BG)

        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.selected_task_id = None
        self.task_rows = {}
        self.filtered_tasks = []

        self.search_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.category_var = tk.StringVar(value="General")
        self.tags_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.status_var = tk.StringVar(value="In Progress")
        self.summary_var = tk.StringVar()
        self.footer_var = tk.StringVar(value="No note selected")
        self.empty_state_var = tk.StringVar()

        self._build_styles()
        self._build_layout()
        self._bind_shortcuts()
        self.search_var.trace_add("write", self._on_search_changed)
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
        shell.columnconfigure(0, weight=0, minsize=320)
        shell.columnconfigure(1, weight=1)
        shell.columnconfigure(2, weight=0, minsize=310)
        shell.rowconfigure(0, weight=1)

        self._build_sidebar(shell)
        self._build_main_content(shell)
        self._build_calendar_panel(shell)

    def _panel(self, parent, padding=18, bg=None):
        return tk.Frame(
            parent,
            bg=bg or self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=padding,
            pady=padding,
        )

    def _build_sidebar(self, parent):
        sidebar = self._panel(parent, padding=16, bg=self.PANEL_SOFT)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(4, weight=1)

        tk.Label(
            sidebar,
            text="Workspace",
            bg=self.PANEL_SOFT,
            fg=self.SUBTLE,
            font=("Segoe UI", 10),
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            sidebar,
            text="Notes",
            bg=self.PANEL_SOFT,
            fg=self.TEXT,
            font=("Georgia", 24, "bold"),
        ).grid(row=1, column=0, sticky="w", pady=(6, 18))

        self.search_entry = self._entry(sidebar, self.search_var)
        self.search_entry.grid(row=2, column=0, sticky="ew")
        tk.Label(
            sidebar,
            text="Search titles, content, tags, categories, or dates",
            bg=self.PANEL_SOFT,
            fg=self.SUBTLE,
            anchor="w",
        ).grid(row=3, column=0, sticky="ew", pady=(6, 14))

        list_shell = tk.Frame(sidebar, bg=self.PANEL_SOFT)
        list_shell.grid(row=4, column=0, sticky="nsew")
        list_shell.columnconfigure(0, weight=1)
        list_shell.rowconfigure(1, weight=1)

        header = tk.Frame(list_shell, bg=self.PANEL_SOFT)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.columnconfigure(0, weight=1)
        tk.Label(
            header,
            text="Library",
            bg=self.PANEL_SOFT,
            fg=self.MUTED,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, sticky="w")
        self._button(header, "New", self._start_new_note, self.PANEL_ALT, width=6).grid(
            row=0, column=1, sticky="e"
        )

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
            wraplength=260,
        ).grid(row=5, column=0, sticky="ew", pady=(18, 0))

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
            text="Daily / Notes",
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
        card.rowconfigure(3, weight=1)

        self.header_date = tk.Label(
            card,
            text=self._format_display_date(datetime.now().strftime("%Y-%m-%d")),
            bg=self.BG,
            fg=self.TEXT,
            font=("Georgia", 27, "bold"),
        )
        self.header_date.grid(row=0, column=0, sticky="w")

        self.chips_frame = tk.Frame(card, bg=self.BG)
        self.chips_frame.grid(row=1, column=0, sticky="w", pady=(12, 20))

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

        self._field_label(properties, "Title").grid(row=1, column=0, sticky="w", pady=6)
        self.title_entry = self._entry(
            properties, self.title_var, font=("Georgia", 14, "bold")
        )
        self.title_entry.grid(row=1, column=1, sticky="ew", pady=6)

        self._field_label(properties, "Category").grid(row=2, column=0, sticky="w", pady=6)
        self.category_entry = self._entry(properties, self.category_var)
        self.category_entry.grid(row=2, column=1, sticky="ew", pady=6)

        self._field_label(properties, "Tags").grid(row=3, column=0, sticky="w", pady=6)
        self.tags_entry = self._entry(properties, self.tags_var)
        self.tags_entry.grid(row=3, column=1, sticky="ew", pady=6)

        self._field_label(properties, "Due date").grid(row=4, column=0, sticky="w", pady=6)
        self.due_date_entry = self._entry(properties, self.due_date_var)
        self.due_date_entry.grid(row=4, column=1, sticky="ew", pady=6)

        self._field_label(properties, "Status").grid(row=5, column=0, sticky="w", pady=6)
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
            font=("Segoe UI", 10),
        )
        self.status_menu["menu"].configure(
            bg=self.PANEL_ALT, fg=self.TEXT, activebackground="#403932"
        )
        self.status_menu.grid(row=5, column=1, sticky="w", pady=6)

        editor_shell = tk.Frame(card, bg=self.BG)
        editor_shell.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        editor_shell.columnconfigure(0, weight=1)
        editor_shell.rowconfigure(1, weight=1)

        tk.Label(
            editor_shell,
            text="Body",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        text_wrap = tk.Frame(editor_shell, bg=self.PANEL_ALT, highlightbackground=self.BORDER, highlightthickness=1)
        text_wrap.grid(row=1, column=0, sticky="nsew")
        text_wrap.columnconfigure(0, weight=1)
        text_wrap.rowconfigure(0, weight=1)

        self.note_text = tk.Text(
            text_wrap,
            wrap="word",
            relief="flat",
            borderwidth=0,
            padx=16,
            pady=16,
            font=("Segoe UI", 11),
            undo=True,
            spacing1=2,
            spacing2=3,
        )
        self.note_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(text_wrap, command=self.note_text.yview, bg=self.PANEL_ALT)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.note_text.configure(yscrollcommand=scrollbar.set)
        self.note_text.bind("<KeyRelease>", self._on_editor_change)

        self.empty_state = tk.Frame(text_wrap, bg=self.PANEL_ALT)
        self.empty_state.grid(row=0, column=0, sticky="nsew")
        self.empty_state.columnconfigure(0, weight=1)
        self.empty_state.rowconfigure(0, weight=1)

        empty_inner = tk.Frame(self.empty_state, bg=self.PANEL_ALT)
        empty_inner.grid(row=0, column=0)
        tk.Label(
            empty_inner,
            text="No note selected",
            bg=self.PANEL_ALT,
            fg=self.TEXT,
            font=("Georgia", 24, "bold"),
        ).pack()
        tk.Label(
            empty_inner,
            textvariable=self.empty_state_var,
            bg=self.PANEL_ALT,
            fg=self.SUBTLE,
            wraplength=420,
            justify="center",
        ).pack(pady=(10, 18))
        self._button(
            empty_inner, "Create a new note", self._start_new_note, self.ACCENT_SOFT
        ).pack()

        footer = tk.Frame(card, bg=self.BG)
        footer.grid(row=4, column=0, sticky="ew", pady=(18, 0))
        footer.columnconfigure(0, weight=1)

        tk.Label(
            footer,
            textvariable=self.footer_var,
            bg=self.BG,
            fg=self.SUBTLE,
        ).grid(row=0, column=0, sticky="w")

        actions = tk.Frame(footer, bg=self.BG)
        actions.grid(row=0, column=1, sticky="e")
        for index in range(4):
            actions.columnconfigure(index, weight=1)

        self._button(actions, "New Note", self._start_new_note, self.PANEL_ALT).grid(
            row=0, column=0, padx=(0, 8)
        )
        self._button(actions, "Duplicate", self._duplicate_note, self.PANEL_ALT).grid(
            row=0, column=1, padx=8
        )
        self._button(actions, "Save Note", self._save_task, self.ACCENT_SOFT).grid(
            row=0, column=2, padx=8
        )
        self._button(actions, "Delete", self._delete_task, "#46312e").grid(
            row=0, column=3, padx=(8, 0)
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

        insights = tk.Frame(panel, bg=self.PANEL)
        insights.grid(row=2, column=0, sticky="ew", pady=(22, 0))
        insights.columnconfigure(0, weight=1)
        tk.Label(
            insights,
            text="Quick Notes",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            insights,
            text="Use due dates for planning. Leave them empty for free-form notes.",
            bg=self.PANEL,
            fg=self.SUBTLE,
            wraplength=230,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        self._render_calendar()

    def _field_label(self, parent, text):
        return tk.Label(
            parent,
            text=text,
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10),
        )

    def _entry(self, parent, variable, font=("Segoe UI", 11)):
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
            font=font,
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

    def _bind_shortcuts(self):
        self.root.bind_class("Entry", "<Control-a>", self._select_all_entry)
        self.root.bind_class("Entry", "<Control-A>", self._select_all_entry)
        self.root.bind_class("Text", "<Control-a>", self._select_all_text)
        self.root.bind_class("Text", "<Control-A>", self._select_all_text)

    def _select_all_entry(self, event):
        event.widget.select_range(0, "end")
        event.widget.icursor("end")
        return "break"

    def _select_all_text(self, event):
        event.widget.tag_add("sel", "1.0", "end-1c")
        event.widget.mark_set("insert", "1.0")
        event.widget.see("insert")
        return "break"

    def _format_display_date(self, due_date):
        if not due_date:
            return "No due date"
        try:
            return datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return due_date

    def _format_sidebar_label(self, task):
        title = task["title"][:28] + "..." if len(task["title"]) > 28 else task["title"]
        snippet = " ".join(task["text"].split())
        snippet = snippet[:34] + "..." if len(snippet) > 34 else snippet
        if not snippet:
            snippet = "Empty note"
        return f"{title}\n{task['category']}  {task['due_date'] or 'No date'}\n{snippet}"

    def _parse_tags(self):
        raw_tags = self.tags_var.get().strip()
        if not raw_tags:
            return []
        return [tag.strip() for tag in raw_tags.split(",") if tag.strip()]

    def _on_search_changed(self, *_args):
        self._load_tasks()

    def _filter_tasks(self, tasks):
        query = self.search_var.get().strip().lower()
        if not query:
            return tasks

        filtered = []
        for task in tasks:
            haystack = " ".join(
                [
                    task["title"],
                    task["text"],
                    task["category"],
                    task["tags"],
                    task["due_date"],
                    task["status"],
                ]
            ).lower()
            if query in haystack:
                filtered.append(task)
        return filtered

    def _load_tasks(self):
        previous_selection = self.selected_task_id
        self.task_listbox.delete(0, tk.END)
        self.task_rows = {}

        tasks = self._filter_tasks(self.manager.list_tasks())
        self.filtered_tasks = tasks

        for index, task in enumerate(tasks):
            self.task_listbox.insert(tk.END, self._format_sidebar_label(task))
            self.task_rows[index] = task["id"]

        total_tasks = len(self.manager.list_tasks())
        visible_tasks = len(tasks)
        completed_tasks = len(
            [task for task in self.manager.list_tasks() if task["status"] == "Completed"]
        )
        dated_tasks = len(
            [task for task in self.manager.list_tasks() if task["due_date"]]
        )
        self.summary_var.set(
            f"Visible: {visible_tasks}\nAll notes: {total_tasks}\nCompleted: {completed_tasks}\nWith due date: {dated_tasks}"
        )

        if previous_selection is not None:
            for index, task_id in self.task_rows.items():
                if task_id == previous_selection:
                    self.task_listbox.selection_set(index)
                    self.task_listbox.activate(index)
                    self._on_listbox_select()
                    return

        if not tasks:
            self.selected_task_id = None
            self._show_empty_state(
                "There are no notes yet. Click the button below if you want to create a new note."
                if not self.manager.list_tasks()
                else "No notes match the current search. Clear the search or create a new note."
            )
        elif self.selected_task_id is None:
            self.task_listbox.selection_set(0)
            self.task_listbox.activate(0)
            self._on_listbox_select()

    def _show_empty_state(self, message):
        self.empty_state_var.set(message)
        self.empty_state.tkraise()
        today = datetime.now().strftime("%Y-%m-%d")
        self.header_date.config(text=today)
        self.date_title.config(text=today)
        self._render_tag_chips({"category": "", "tags": "", "due_date": ""})
        self.footer_var.set("No note selected")

    def _hide_empty_state(self):
        self.note_text.tkraise()

    def _start_new_note(self):
        self.selected_task_id = None
        self.task_listbox.selection_clear(0, tk.END)
        self._hide_empty_state()
        self.footer_var.set("Draft note")
        if not self.title_var.get().strip() and not self.note_text.get("1.0", tk.END).strip():
            self.category_var.set("General")
            self.tags_var.set("")
            self.due_date_var.set("")
            self.status_var.set("In Progress")
        self.title_entry.focus_set()

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
        self.title_var.set(task["title"])
        self.note_text.delete("1.0", tk.END)
        self.note_text.insert("1.0", task["text"])
        self.category_var.set(task["category"])
        self.tags_var.set(task["tags"])
        self.due_date_var.set(task["due_date"])
        self.status_var.set(task["status"])
        display_date = task["due_date"] or datetime.now().strftime("%Y-%m-%d")
        self.header_date.config(text=self._format_display_date(display_date))
        self.date_title.config(text=self._format_display_date(display_date))
        self._render_tag_chips(task)
        self._hide_empty_state()
        self._update_footer(task["text"])

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
        if task.get("status"):
            chips.append((task["status"], "#3a332f", self.MUTED))

        if not chips:
            chips.append(("No properties yet", self.PANEL_ALT, self.SUBTLE))

        for index, (text, bg, fg) in enumerate(chips):
            tk.Label(
                self.chips_frame,
                text=text,
                bg=bg,
                fg=fg,
                padx=10,
                pady=4,
                font=("Segoe UI", 9, "bold"),
            ).grid(row=0, column=index, padx=(0, 8), sticky="w")

    def _clear_form(self):
        self.selected_task_id = None
        self.task_listbox.selection_clear(0, tk.END)
        self.title_var.set("")
        self.note_text.delete("1.0", tk.END)
        self.category_var.set("General")
        self.tags_var.set("")
        self.due_date_var.set("")
        self.status_var.set("In Progress")
        self._show_empty_state(
            "Write a title, add a note body, and press Save Note when you are ready."
        )

    def _update_footer(self, text):
        words = len(text.split())
        characters = len(text)
        lines = max(1, int(self.note_text.index("end-1c").split(".")[0]))
        self.footer_var.set(
            f"Words: {words}    Characters: {characters}    Lines: {lines}"
        )

    def _on_editor_change(self, _event=None):
        self._update_footer(self.note_text.get("1.0", tk.END).strip())

    def _save_task(self):
        content = self.note_text.get("1.0", tk.END).strip()
        try:
            if self.selected_task_id is None:
                task_id = self.manager.create_task(
                    self.title_var.get(),
                    content,
                    self.category_var.get(),
                    self._parse_tags(),
                    self.due_date_var.get(),
                )
                self.selected_task_id = task_id
            else:
                self.manager.update_task_details(
                    self.selected_task_id,
                    self.title_var.get(),
                    content,
                    self.category_var.get(),
                    self._parse_tags(),
                    self.due_date_var.get(),
                )
                self.manager.change_task_status(self.selected_task_id, self.status_var.get())

            self._load_tasks()
            self._select_current_task()
            messagebox.showinfo("Saved", "Note saved successfully.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to save note: {error}")

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

    def _duplicate_note(self):
        content = self.note_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Nothing to duplicate", "Open or write a note first.")
            return

        try:
            task_id = self.manager.create_task(
                f"{self.title_var.get() or 'Untitled note'} (Copy)",
                content,
                self.category_var.get(),
                self._parse_tags(),
                self.due_date_var.get(),
            )
            self.selected_task_id = task_id
            self._load_tasks()
            self._select_current_task()
            messagebox.showinfo("Duplicated", "A copy of the note was created.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to duplicate note: {error}")

    def _delete_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning("No selection", "Select a note first.")
            return

        if not messagebox.askyesno(
            "Delete note", "Do you want to delete the selected note?"
        ):
            return

        previous_index = None
        current_selection = self.task_listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
            previous_index = current_index - 1 if current_index > 0 else 0

        try:
            self.manager.remove_task(self.selected_task_id)
            self.selected_task_id = None
            self._load_tasks()

            if self.filtered_tasks:
                if previous_index is None:
                    previous_index = 0
                previous_index = min(previous_index, len(self.filtered_tasks) - 1)
                self.task_listbox.selection_clear(0, tk.END)
                self.task_listbox.selection_set(previous_index)
                self.task_listbox.activate(previous_index)
                self._on_listbox_select()
            else:
                self._clear_form()

            messagebox.showinfo("Deleted", "Note deleted successfully.")
        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))
        except Exception as error:
            messagebox.showerror("Error", f"Unable to delete note: {error}")

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
        due_dates = {
            task["due_date"]
            for task in self.manager.list_tasks()
            if task["due_date"]
            and task["due_date"].startswith(f"{self.current_year:04d}-{self.current_month:02d}")
        }
        for row_index, week in enumerate(
            cal.monthdatescalendar(self.current_year, self.current_month), start=1
        ):
            for col_index, day in enumerate(week):
                is_current = day.month == self.current_month
                is_today = day == today
                date_key = day.strftime("%Y-%m-%d")
                has_due = date_key in due_dates
                bg = self.PANEL if is_current else self.PANEL_ALT
                fg = self.TEXT if is_current else self.SUBTLE
                if has_due:
                    bg = "#3b4a3d"
                    fg = self.ACCENT
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
                    font=("Segoe UI", 10, "bold" if is_today or has_due else "normal"),
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
