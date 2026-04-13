from __future__ import annotations

import sys
from datetime import datetime, timedelta

from PySide6.QtCore import QDate, QTimer, Qt
from PySide6.QtGui import QAction, QFont, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from task_manager import TaskManager


APP_STYLE = """
QMainWindow, QWidget { background: #23211f; color: #ead0ae; font-family: 'Segoe UI'; font-size: 14px; }
QFrame#panel { background: #2c2825; border: 1px solid #3b3531; border-radius: 14px; }
QFrame#mainPanel { background: #23211f; border: 1px solid #3b3531; border-radius: 16px; }
QLineEdit, QTextEdit, QComboBox, QListWidget, QCalendarWidget QWidget#qt_calendar_navigationbar { background: #312c29; color: #ead0ae; }
QLineEdit, QTextEdit, QComboBox { border: 1px solid #3b3531; border-radius: 10px; padding: 10px 12px; selection-background-color: #4b433d; }
QListWidget { border: 1px solid #3b3531; border-radius: 12px; padding: 8px; outline: none; }
QListWidget::item { padding: 12px; margin: 4px 0px; border-radius: 12px; }
QListWidget::item:selected { background: #4b433d; color: #ead0ae; }
QPushButton, QToolButton { background: #312c29; color: #ead0ae; border: 1px solid #3b3531; border-radius: 10px; padding: 10px 14px; font-weight: 600; }
QPushButton:hover, QToolButton:hover { background: #3a342f; }
QPushButton#accentButton, QToolButton#accentButton { background: #3b4a3d; color: #8ecf8b; border-color: #465646; }
QPushButton#dangerButton { background: #46312e; color: #dba7a0; border-color: #5a3c37; }
QToolButton#filterChip { border-radius: 14px; padding: 6px 12px; }
QToolButton#filterChip:checked { background: #343c52; color: #c8d7ff; border-color: #495474; }
QLabel#titleText { font-family: 'Georgia'; font-size: 30px; font-weight: 700; }
QLabel#sectionTitle { font-size: 18px; font-weight: 700; }
QLabel#muted { color: #8f7f6c; }
QLabel#chip { background: #343c52; color: #c8d7ff; border-radius: 9px; padding: 4px 10px; font-size: 12px; font-weight: 600; }
QCalendarWidget { border: none; border-radius: 12px; }
QCalendarWidget QToolButton { background: transparent; border: none; color: #ead0ae; }
QCalendarWidget QAbstractItemView:enabled { background: #2c2825; color: #ead0ae; selection-background-color: #8ecf8b; selection-color: #1a2218; }
QSplitter::handle { background: #23211f; width: 8px; }
"""


class NotesMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.selected_note_id = None
        self.filtered_notes = []
        self.calendar_visible = True
        self.current_filter = "all"
        self.loading_note = False

        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(1200)
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.timeout.connect(self._autosave_note)

        self.setWindowTitle("Todo Manager")
        self.resize(1520, 920)
        self.setMinimumSize(1280, 780)

        self._build_ui()
        self._load_notes()

    def _build_ui(self):
        self._create_actions()

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(12)

        root_layout.addWidget(self._build_header())

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        root_layout.addWidget(self.splitter, 1)

        self.sidebar_panel = self._build_sidebar()
        self.main_panel = self._build_editor()
        self.calendar_panel = self._build_calendar_panel()

        self.splitter.addWidget(self.sidebar_panel)
        self.splitter.addWidget(self.main_panel)
        self.splitter.addWidget(self.calendar_panel)
        self.splitter.setSizes([340, 860, 280])

    def _create_actions(self):
        actions = [
            ("Toggle Calendar", "Ctrl+\\", self._toggle_calendar_panel),
            ("New Note", QKeySequence.New, self._start_new_note),
            ("Save Note", QKeySequence.Save, self._save_note),
            ("Focus Search", QKeySequence.Find, self._focus_search),
            ("Duplicate Note", "Ctrl+D", self._duplicate_note),
        ]
        for name, shortcut, callback in actions:
            action = QAction(name, self)
            action.setShortcut(shortcut)
            action.triggered.connect(callback)
            self.addAction(action)

    def _build_header(self):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(8, 0, 8, 0)

        left = QVBoxLayout()
        breadcrumb = QLabel("Daily / Notes")
        breadcrumb.setObjectName("muted")
        title = QLabel("Workspace")
        title.setFont(QFont("Georgia", 22, QFont.Bold))
        left.addWidget(breadcrumb)
        left.addWidget(title)
        layout.addLayout(left)
        layout.addStretch(1)

        self.header_date_label = QLabel(datetime.now().strftime("%Y-%m-%d"))
        self.header_date_label.setFont(QFont("Georgia", 14))
        layout.addWidget(self.header_date_label)

        self.sync_label = QLabel("Ready")
        self.sync_label.setObjectName("muted")
        layout.addWidget(self.sync_label)

        self.pin_button = QToolButton()
        self.pin_button.setText("Pin")
        self.pin_button.setCheckable(True)
        self.pin_button.clicked.connect(self._toggle_pin)
        layout.addWidget(self.pin_button)

        self.toggle_calendar_button = QToolButton()
        self.toggle_calendar_button.setText("Hide Calendar")
        self.toggle_calendar_button.clicked.connect(self._toggle_calendar_panel)
        layout.addWidget(self.toggle_calendar_button)
        return frame

    def _build_sidebar(self):
        panel = QFrame()
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        caption = QLabel("Library")
        caption.setObjectName("muted")
        heading = QLabel("Notes")
        heading.setFont(QFont("Georgia", 24, QFont.Bold))
        layout.addWidget(caption)
        layout.addWidget(heading)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search titles, content, tags, dates...")
        self.search_input.textChanged.connect(self._load_notes)
        layout.addWidget(self.search_input)

        filters = QHBoxLayout()
        filters.setSpacing(8)
        self.filter_buttons = {}
        for key, label in [("all", "All"), ("pinned", "Pinned"), ("due", "Due Soon"), ("completed", "Completed")]:
            button = QToolButton()
            button.setText(label)
            button.setCheckable(True)
            button.setObjectName("filterChip")
            button.clicked.connect(lambda checked, mode=key: self._set_filter(mode))
            self.filter_buttons[key] = button
            filters.addWidget(button)
        filters.addStretch(1)
        layout.addLayout(filters)
        self.filter_buttons["all"].setChecked(True)

        self.new_button = QPushButton("New Note")
        self.new_button.setObjectName("accentButton")
        self.new_button.clicked.connect(self._start_new_note)
        layout.addWidget(self.new_button)

        self.notes_list = QListWidget()
        self.notes_list.itemSelectionChanged.connect(self._on_note_selected)
        layout.addWidget(self.notes_list, 1)

        self.summary_label = QLabel()
        self.summary_label.setObjectName("muted")
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)
        return panel

    def _build_editor(self):
        panel = QFrame()
        panel.setObjectName("mainPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        self.note_date_label = QLabel(datetime.now().strftime("%Y-%m-%d"))
        self.note_date_label.setObjectName("titleText")
        layout.addWidget(self.note_date_label)

        self.chips_row = QHBoxLayout()
        self.chips_row.setSpacing(8)
        layout.addLayout(self.chips_row)

        properties_title = QLabel("Properties")
        properties_title.setObjectName("sectionTitle")
        layout.addWidget(properties_title)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Untitled note")
        self.title_input.textChanged.connect(self._on_editor_modified)
        layout.addWidget(self._labeled_widget("Title", self.title_input))

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("General")
        self.category_input.textChanged.connect(self._on_editor_modified)
        layout.addWidget(self._labeled_widget("Category", self.category_input))

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("daily, todo, idea")
        self.tags_input.textChanged.connect(self._on_editor_modified)
        layout.addWidget(self._labeled_widget("Tags", self.tags_input))

        self.due_date_input = QLineEdit()
        self.due_date_input.setPlaceholderText("YYYY-MM-DD")
        self.due_date_input.textChanged.connect(self._sync_due_date_header)
        self.due_date_input.textChanged.connect(self._on_editor_modified)
        layout.addWidget(self._labeled_widget("Due date", self.due_date_input))

        self.status_input = QComboBox()
        self.status_input.addItems(["In Progress", "Completed", "Not Completed"])
        self.status_input.currentTextChanged.connect(self._on_editor_modified)
        layout.addWidget(self._labeled_widget("Status", self.status_input))

        body_title = QLabel("Body")
        body_title.setObjectName("sectionTitle")
        layout.addWidget(body_title)

        self.editor_stack = QSplitter(Qt.Vertical)
        self.editor_stack.setChildrenCollapsible(False)
        self.editor_stack.setHandleWidth(6)

        self.body_editor = QTextEdit()
        self.body_editor.setPlaceholderText("Start writing your note here...")
        self.body_editor.textChanged.connect(self._on_editor_modified)
        self.editor_stack.addWidget(self.body_editor)

        self.empty_state = self._build_empty_state()
        self.editor_stack.addWidget(self.empty_state)
        self.editor_stack.setSizes([700, 0])
        layout.addWidget(self.editor_stack, 1)

        footer = QHBoxLayout()
        self.footer_stats = QLabel("No note selected")
        self.footer_stats.setObjectName("muted")
        footer.addWidget(self.footer_stats)
        footer.addStretch(1)

        self.duplicate_button = QPushButton("Duplicate")
        self.duplicate_button.clicked.connect(self._duplicate_note)
        self.save_button = QPushButton("Save Note")
        self.save_button.setObjectName("accentButton")
        self.save_button.clicked.connect(self._save_note)
        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("dangerButton")
        self.delete_button.clicked.connect(self._delete_note)

        footer.addWidget(self.duplicate_button)
        footer.addWidget(self.save_button)
        footer.addWidget(self.delete_button)
        layout.addLayout(footer)
        return panel

    def _build_empty_state(self):
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.addStretch(1)
        title = QLabel("No note selected")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Georgia", 22, QFont.Bold))
        text = QLabel("Select a note from the sidebar or press Create a new note to begin writing.")
        text.setObjectName("muted")
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignCenter)
        button = QPushButton("Create a new note")
        button.setObjectName("accentButton")
        button.clicked.connect(self._start_new_note)
        layout.addWidget(title)
        layout.addWidget(text)
        layout.addSpacing(12)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        return wrapper

    def _build_calendar_panel(self):
        panel = QFrame()
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        title = QLabel("Calendar")
        title.setFont(QFont("Georgia", 22, QFont.Bold))
        layout.addWidget(title)

        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setGridVisible(False)
        self.calendar_widget.clicked.connect(self._apply_calendar_date)
        layout.addWidget(self.calendar_widget)

        self.calendar_stats = QLabel()
        self.calendar_stats.setObjectName("muted")
        self.calendar_stats.setWordWrap(True)
        layout.addWidget(self.calendar_stats)
        layout.addStretch(1)
        return panel

    def _labeled_widget(self, text, widget):
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        label = QLabel(text)
        label.setObjectName("muted")
        layout.addWidget(label)
        layout.addWidget(widget)
        return wrapper

    def _focus_search(self):
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _set_filter(self, mode):
        self.current_filter = mode
        for key, button in self.filter_buttons.items():
            button.setChecked(key == mode)
        self._load_notes()

    def _toggle_calendar_panel(self):
        self.calendar_visible = not self.calendar_visible
        self.calendar_panel.setVisible(self.calendar_visible)
        self.toggle_calendar_button.setText("Hide Calendar" if self.calendar_visible else "Show Calendar")
        self.splitter.setSizes([340, 860, 280] if self.calendar_visible else [360, 1120, 0])

    def _apply_calendar_date(self, selected_date: QDate):
        self.due_date_input.setText(selected_date.toString("yyyy-MM-dd"))

    def _filter_notes_for_due_soon(self, notes):
        now = datetime.now().date()
        due_limit = now + timedelta(days=7)
        results = []
        for note in notes:
            if not note["due_date"]:
                continue
            try:
                due_date = datetime.strptime(note["due_date"], "%Y-%m-%d").date()
            except ValueError:
                continue
            if due_date <= due_limit:
                results.append(note)
        return results

    def _filter_notes(self, notes):
        query = self.search_input.text().strip().lower()
        due_soon = {note["id"] for note in self._filter_notes_for_due_soon(notes)}
        filtered = []
        for note in notes:
            haystack = " ".join([note["title"], note["text"], note["category"], note["tags"], note["due_date"], note["status"]]).lower()
            if query and query not in haystack:
                continue
            if self.current_filter == "pinned" and not note.get("pinned"):
                continue
            if self.current_filter == "completed" and note["status"] != "Completed":
                continue
            if self.current_filter == "due" and note["id"] not in due_soon:
                continue
            filtered.append(note)
        return filtered

    def _note_preview(self, note):
        pin = "● " if note.get("pinned") else ""
        title = pin + (note["title"] or "Untitled note")
        snippet = " ".join(note["text"].split())
        if len(snippet) > 52:
            snippet = snippet[:52] + "..."
        updated = (note.get("updated_at", "") or "").replace("T", " ")[:16]
        meta = f"{note['category']}  {note['due_date'] or 'No date'}  {updated}"
        return f"{title}\n{meta}\n{snippet or 'Empty note'}"

    def _load_notes(self):
        previous = self.selected_note_id
        all_notes = self.manager.list_tasks()
        self.filtered_notes = self._filter_notes(all_notes)

        self.notes_list.clear()
        for note in self.filtered_notes:
            item = QListWidgetItem(self._note_preview(note))
            item.setData(Qt.UserRole, note["id"])
            item.setSizeHint(item.sizeHint() * 1.4)
            self.notes_list.addItem(item)

        completed = len([note for note in all_notes if note["status"] == "Completed"])
        due = len([note for note in all_notes if note["due_date"]])
        pinned = len([note for note in all_notes if note.get("pinned")])
        self.summary_label.setText(
            f"Visible: {len(self.filtered_notes)}\nAll notes: {len(all_notes)}\nPinned: {pinned}\nCompleted: {completed}\nWith due date: {due}"
        )
        self.calendar_stats.setText(
            f"Upcoming in 7 days: {len(self._filter_notes_for_due_soon(all_notes))}\nToggle the panel with Ctrl+\\ when you want more writing space."
        )

        if previous is not None:
            for row in range(self.notes_list.count()):
                item = self.notes_list.item(row)
                if item.data(Qt.UserRole) == previous:
                    self.notes_list.setCurrentRow(row)
                    return

        if self.filtered_notes and self.selected_note_id is None:
            self.notes_list.setCurrentRow(0)
        elif not self.filtered_notes:
            self.selected_note_id = None
            self._show_empty_state()

    def _show_empty_state(self):
        self.body_editor.hide()
        self.empty_state.show()
        self.footer_stats.setText("No note selected")
        today = datetime.now().strftime("%Y-%m-%d")
        self.note_date_label.setText(today)
        self.header_date_label.setText(today)
        self._render_chips([])
        self.pin_button.setChecked(False)

    def _show_editor(self):
        self.empty_state.hide()
        self.body_editor.show()

    def _render_chips(self, chips):
        while self.chips_row.count():
            item = self.chips_row.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        if not chips:
            placeholder = QLabel("No properties yet")
            placeholder.setObjectName("muted")
            self.chips_row.addWidget(placeholder)
            self.chips_row.addStretch(1)
            return
        for chip_text in chips:
            chip = QLabel(chip_text)
            chip.setObjectName("chip")
            self.chips_row.addWidget(chip)
        self.chips_row.addStretch(1)

    def _format_display_date(self, value):
        if not value:
            return "No due date"
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return value

    def _on_note_selected(self):
        item = self.notes_list.currentItem()
        if not item:
            return
        note = self.manager.get_task(item.data(Qt.UserRole))
        if not note:
            return
        self.loading_note = True
        self.selected_note_id = note["id"]
        self.title_input.setText(note["title"])
        self.body_editor.setPlainText(note["text"])
        self.category_input.setText(note["category"])
        self.tags_input.setText(note["tags"])
        self.due_date_input.setText(note["due_date"])
        self.status_input.setCurrentText(note["status"])
        self.pin_button.setChecked(note.get("pinned", False))
        display_date = note["due_date"] or datetime.now().strftime("%Y-%m-%d")
        self.note_date_label.setText(self._format_display_date(display_date))
        self.header_date_label.setText(self._format_display_date(display_date))
        chips = [note["category"], note["status"]]
        chips.extend(f"#{tag.strip()}" for tag in note["tags"].split(",") if tag.strip())
        if note["due_date"]:
            chips.append(note["due_date"])
        if note.get("pinned"):
            chips.append("Pinned")
        self._render_chips(chips)
        self._update_footer_stats()
        self._show_editor()
        self.loading_note = False

    def _sync_due_date_header(self):
        value = self.due_date_input.text().strip()
        text = self._format_display_date(value or "")
        self.note_date_label.setText(text)
        self.header_date_label.setText(text)

    def _update_footer_stats(self):
        text = self.body_editor.toPlainText()
        words = len(text.split())
        chars = len(text)
        lines = max(1, text.count("\n") + 1 if text else 1)
        self.footer_stats.setText(f"Words: {words}    Characters: {chars}    Lines: {lines}")

    def _on_editor_modified(self):
        if self.loading_note:
            return
        self._update_footer_stats()
        if self.title_input.text().strip() or self.body_editor.toPlainText().strip():
            self.sync_label.setText("Editing...")
            self.autosave_timer.start()

    def _collect_editor_state(self):
        return {
            "title": self.title_input.text(),
            "body": self.body_editor.toPlainText(),
            "category": self.category_input.text(),
            "tags": [tag.strip() for tag in self.tags_input.text().split(",") if tag.strip()],
            "due_date": self.due_date_input.text().strip(),
            "status": self.status_input.currentText(),
            "pinned": self.pin_button.isChecked(),
        }

    def _start_new_note(self):
        self.loading_note = True
        self.selected_note_id = None
        self.notes_list.clearSelection()
        self.title_input.clear()
        self.body_editor.clear()
        self.category_input.setText("General")
        self.tags_input.clear()
        self.due_date_input.clear()
        self.status_input.setCurrentText("In Progress")
        self.pin_button.setChecked(False)
        self._show_editor()
        self._render_chips([])
        self._update_footer_stats()
        today = datetime.now().strftime("%Y-%m-%d")
        self.note_date_label.setText(today)
        self.header_date_label.setText(today)
        self.sync_label.setText("Draft")
        self.loading_note = False
        self.title_input.setFocus()

    def _autosave_note(self):
        self._save_note(silent=True)

    def _save_note(self, silent=False):
        data = self._collect_editor_state()
        try:
            if self.selected_note_id is None:
                self.selected_note_id = self.manager.create_task(
                    data["title"], data["body"], data["category"], data["tags"], data["due_date"], data["pinned"]
                )
            else:
                self.manager.update_task_details(
                    self.selected_note_id,
                    data["title"],
                    data["body"],
                    data["category"],
                    data["tags"],
                    data["due_date"],
                    data["pinned"],
                )
                self.manager.change_task_status(self.selected_note_id, data["status"])
            self.sync_label.setText("Autosaved" if silent else "Saved")
            current = self.selected_note_id
            self._load_notes()
            self.selected_note_id = current
            if not silent:
                QMessageBox.information(self, "Saved", "Note saved successfully.")
        except ValueError as error:
            self.sync_label.setText("Needs attention")
            if not silent:
                QMessageBox.warning(self, "Validation Error", str(error))
        except Exception as error:
            self.sync_label.setText("Save failed")
            if not silent:
                QMessageBox.critical(self, "Error", f"Unable to save note: {error}")

    def _toggle_pin(self):
        if self.loading_note:
            return
        self._on_editor_modified()

    def _duplicate_note(self):
        data = self._collect_editor_state()
        if not data["title"] and not data["body"]:
            QMessageBox.information(self, "Nothing to duplicate", "Open or write a note first.")
            return
        try:
            self.selected_note_id = self.manager.create_task(
                f"{data['title'] or 'Untitled note'} (Copy)",
                data["body"],
                data["category"],
                data["tags"],
                data["due_date"],
                data["pinned"],
            )
            self.sync_label.setText("Duplicated")
            self._load_notes()
            QMessageBox.information(self, "Duplicated", "A copy of the note was created.")
        except ValueError as error:
            QMessageBox.warning(self, "Validation Error", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Unable to duplicate note: {error}")

    def _delete_note(self):
        if self.selected_note_id is None:
            QMessageBox.information(self, "No selection", "Select a note first.")
            return
        result = QMessageBox.question(self, "Delete note", "Do you want to delete the selected note?", QMessageBox.Yes | QMessageBox.No)
        if result != QMessageBox.Yes:
            return
        current_row = self.notes_list.currentRow()
        target_row = max(0, current_row - 1)
        try:
            self.manager.remove_task(self.selected_note_id)
            self.selected_note_id = None
            self.sync_label.setText("Deleted")
            self._load_notes()
            if self.notes_list.count():
                self.notes_list.setCurrentRow(min(target_row, self.notes_list.count() - 1))
            else:
                self._show_empty_state()
            QMessageBox.information(self, "Deleted", "Note deleted successfully.")
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Unable to delete note: {error}")


def run_qt_app():
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = NotesMainWindow()
    window.show()
    return app.exec()
