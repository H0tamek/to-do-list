from __future__ import annotations

import sys
from datetime import datetime

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QAction, QFont
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
    QSizePolicy,
    QSplitter,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from task_manager import TaskManager


APP_STYLE = """
QMainWindow, QWidget {
    background: #23211f;
    color: #ead0ae;
    font-family: 'Segoe UI';
    font-size: 14px;
}
QFrame#panel {
    background: #2c2825;
    border: 1px solid #3b3531;
    border-radius: 14px;
}
QFrame#mainPanel {
    background: #23211f;
    border: 1px solid #3b3531;
    border-radius: 16px;
}
QLineEdit, QTextEdit, QComboBox, QListWidget, QCalendarWidget QWidget#qt_calendar_navigationbar {
    background: #312c29;
    color: #ead0ae;
}
QLineEdit, QTextEdit, QComboBox {
    border: 1px solid #3b3531;
    border-radius: 10px;
    padding: 10px 12px;
    selection-background-color: #4b433d;
}
QListWidget {
    border: 1px solid #3b3531;
    border-radius: 12px;
    padding: 8px;
    outline: none;
}
QListWidget::item {
    padding: 12px;
    margin: 4px 0px;
    border-radius: 10px;
}
QListWidget::item:selected {
    background: #4b433d;
    color: #ead0ae;
}
QPushButton, QToolButton {
    background: #312c29;
    color: #ead0ae;
    border: 1px solid #3b3531;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}
QPushButton:hover, QToolButton:hover {
    background: #3a342f;
}
QPushButton#accentButton {
    background: #3b4a3d;
    color: #8ecf8b;
    border-color: #465646;
}
QPushButton#dangerButton {
    background: #46312e;
    color: #dba7a0;
    border-color: #5a3c37;
}
QLabel#titleText {
    font-family: 'Georgia';
    font-size: 30px;
    font-weight: 700;
}
QLabel#sectionTitle {
    font-size: 18px;
    font-weight: 700;
}
QLabel#muted {
    color: #8f7f6c;
}
QLabel#chip {
    background: #343c52;
    color: #c8d7ff;
    border-radius: 9px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
}
QCalendarWidget {
    border: none;
    border-radius: 12px;
}
QCalendarWidget QToolButton {
    background: transparent;
    border: none;
    color: #ead0ae;
}
QCalendarWidget QAbstractItemView:enabled {
    background: #2c2825;
    color: #ead0ae;
    selection-background-color: #8ecf8b;
    selection-color: #1a2218;
}
QSplitter::handle {
    background: #23211f;
    width: 8px;
}
"""


class NotesMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = TaskManager()
        self.selected_note_id = None
        self.filtered_notes = []
        self.calendar_visible = True

        self.setWindowTitle("Todo Manager")
        self.resize(1480, 900)
        self.setMinimumSize(1260, 760)

        self._build_ui()
        self._load_notes()

    def _build_ui(self):
        self._create_actions()

        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(12)

        header = self._build_header()
        root_layout.addWidget(header)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        root_layout.addWidget(self.splitter, 1)

        self.sidebar_panel = self._build_sidebar()
        self.main_panel = self._build_editor()
        self.calendar_panel = self._build_calendar_panel()

        self.splitter.addWidget(self.sidebar_panel)
        self.splitter.addWidget(self.main_panel)
        self.splitter.addWidget(self.calendar_panel)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 0)
        self.splitter.setSizes([320, 800, 280])

    def _create_actions(self):
        toggle_calendar_action = QAction("Toggle Calendar", self)
        toggle_calendar_action.setShortcut("Ctrl+\\")
        toggle_calendar_action.triggered.connect(self._toggle_calendar_panel)
        self.addAction(toggle_calendar_action)

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

        top_actions = QHBoxLayout()
        self.new_button = QPushButton("New Note")
        self.new_button.clicked.connect(self._start_new_note)
        top_actions.addWidget(self.new_button)
        top_actions.addStretch(1)
        layout.addLayout(top_actions)

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
        self.title_input.textChanged.connect(self._sync_preview_title)
        layout.addWidget(self._labeled_widget("Title", self.title_input))

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("General")
        layout.addWidget(self._labeled_widget("Category", self.category_input))

        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("daily, todo, idea")
        layout.addWidget(self._labeled_widget("Tags", self.tags_input))

        self.due_date_input = QLineEdit()
        self.due_date_input.setPlaceholderText("YYYY-MM-DD")
        self.due_date_input.textChanged.connect(self._sync_due_date_header)
        layout.addWidget(self._labeled_widget("Due date", self.due_date_input))

        self.status_input = QComboBox()
        self.status_input.addItems(["In Progress", "Completed", "Not Completed"])
        layout.addWidget(self._labeled_widget("Status", self.status_input))

        body_title = QLabel("Body")
        body_title.setObjectName("sectionTitle")
        layout.addWidget(body_title)

        self.body_stack = QSplitter(Qt.Vertical)
        self.body_stack.setChildrenCollapsible(False)
        self.body_stack.setHandleWidth(6)

        self.body_editor = QTextEdit()
        self.body_editor.setPlaceholderText("Start writing your note here...")
        self.body_editor.textChanged.connect(self._update_footer_stats)
        self.body_editor.textChanged.connect(self._sync_preview_title)
        self.body_stack.addWidget(self.body_editor)

        self.empty_state = self._build_empty_state()
        self.body_stack.addWidget(self.empty_state)
        self.body_stack.setSizes([700, 0])
        layout.addWidget(self.body_stack, 1)

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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)

        title = QLabel("No note selected")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Georgia", 22, QFont.Bold))
        text = QLabel(
            "Select a note from the sidebar or press Create a new note to begin writing."
        )
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

        hint = QLabel(
            "Click a date to assign it as the current note due date. Use the toggle in the header to hide this panel."
        )
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        layout.addWidget(hint)
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

    def _toggle_calendar_panel(self):
        self.calendar_visible = not self.calendar_visible
        self.calendar_panel.setVisible(self.calendar_visible)
        self.toggle_calendar_button.setText(
            "Hide Calendar" if self.calendar_visible else "Show Calendar"
        )
        if self.calendar_visible:
            self.splitter.setSizes([320, 800, 280])
        else:
            self.splitter.setSizes([360, 1040, 0])

    def _apply_calendar_date(self, selected_date: QDate):
        self.due_date_input.setText(selected_date.toString("yyyy-MM-dd"))

    def _format_display_date(self, value: str) -> str:
        if not value:
            return "No due date"
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return value

    def _note_preview(self, note: dict) -> str:
        title = note["title"] or "Untitled note"
        snippet = " ".join(note["text"].split())
        if len(snippet) > 46:
            snippet = snippet[:46] + "..."
        meta = f"{note['category']}  {note['due_date'] or 'No date'}"
        return f"{title}\n{meta}\n{snippet or 'Empty note'}"

    def _filter_notes(self, notes: list[dict]) -> list[dict]:
        query = self.search_input.text().strip().lower()
        if not query:
            return notes

        filtered = []
        for note in notes:
            haystack = " ".join(
                [
                    note["title"],
                    note["text"],
                    note["category"],
                    note["tags"],
                    note["due_date"],
                    note["status"],
                ]
            ).lower()
            if query in haystack:
                filtered.append(note)
        return filtered

    def _load_notes(self):
        previous = self.selected_note_id
        all_notes = self.manager.list_tasks()
        self.filtered_notes = self._filter_notes(all_notes)

        self.notes_list.clear()
        for note in self.filtered_notes:
            item = QListWidgetItem(self._note_preview(note))
            item.setData(Qt.UserRole, note["id"])
            item.setSizeHint(item.sizeHint() * 1.35)
            self.notes_list.addItem(item)

        completed = len([note for note in all_notes if note["status"] == "Completed"])
        due = len([note for note in all_notes if note["due_date"]])
        self.summary_label.setText(
            f"Visible: {len(self.filtered_notes)}\nAll notes: {len(all_notes)}\nCompleted: {completed}\nWith due date: {due}"
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
        self.note_date_label.setText(datetime.now().strftime("%Y-%m-%d"))
        self.header_date_label.setText(datetime.now().strftime("%Y-%m-%d"))
        self._render_chips([])

    def _show_editor(self):
        self.empty_state.hide()
        self.body_editor.show()

    def _on_note_selected(self):
        item = self.notes_list.currentItem()
        if not item:
            return

        note_id = item.data(Qt.UserRole)
        note = self.manager.get_task(note_id)
        if not note:
            return

        self.selected_note_id = note_id
        self.title_input.setText(note["title"])
        self.body_editor.setPlainText(note["text"])
        self.category_input.setText(note["category"])
        self.tags_input.setText(note["tags"])
        self.due_date_input.setText(note["due_date"])
        self.status_input.setCurrentText(note["status"])
        display_date = note["due_date"] or datetime.now().strftime("%Y-%m-%d")
        self.note_date_label.setText(self._format_display_date(display_date))
        self.header_date_label.setText(self._format_display_date(display_date))
        self._render_chips(
            [note["category"]]
            + [f"#{tag.strip()}" for tag in note["tags"].split(",") if tag.strip()]
            + ([note["due_date"]] if note["due_date"] else [])
        )
        self._update_footer_stats()
        self._show_editor()

    def _render_chips(self, chips: list[str]):
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

    def _sync_due_date_header(self):
        value = self.due_date_input.text().strip()
        self.note_date_label.setText(self._format_display_date(value or ""))
        self.header_date_label.setText(self._format_display_date(value or ""))

    def _sync_preview_title(self):
        title = self.title_input.text().strip()
        if self.selected_note_id is None and title:
            self.footer_stats.setText("Draft note")

    def _update_footer_stats(self):
        text = self.body_editor.toPlainText()
        words = len(text.split())
        chars = len(text)
        lines = max(1, text.count("\n") + 1 if text else 1)
        self.footer_stats.setText(
            f"Words: {words}    Characters: {chars}    Lines: {lines}"
        )

    def _start_new_note(self):
        self.selected_note_id = None
        self.notes_list.clearSelection()
        self.title_input.clear()
        self.body_editor.clear()
        self.category_input.setText("General")
        self.tags_input.clear()
        self.due_date_input.clear()
        self.status_input.setCurrentText("In Progress")
        self._show_editor()
        self._update_footer_stats()
        self.note_date_label.setText(datetime.now().strftime("%Y-%m-%d"))
        self.header_date_label.setText(datetime.now().strftime("%Y-%m-%d"))
        self._render_chips([])
        self.title_input.setFocus()

    def _save_note(self):
        title = self.title_input.text()
        body = self.body_editor.toPlainText()
        category = self.category_input.text()
        tags = [tag.strip() for tag in self.tags_input.text().split(",") if tag.strip()]
        due_date = self.due_date_input.text().strip()
        status = self.status_input.currentText()

        try:
            if self.selected_note_id is None:
                note_id = self.manager.create_task(title, body, category, tags, due_date)
                self.selected_note_id = note_id
            else:
                self.manager.update_task_details(
                    self.selected_note_id, title, body, category, tags, due_date
                )
                self.manager.change_task_status(self.selected_note_id, status)

            self._load_notes()
            QMessageBox.information(self, "Saved", "Note saved successfully.")
        except ValueError as error:
            QMessageBox.warning(self, "Validation Error", str(error))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Unable to save note: {error}")

    def _duplicate_note(self):
        title = self.title_input.text().strip()
        body = self.body_editor.toPlainText().strip()
        if not title and not body:
            QMessageBox.information(self, "Nothing to duplicate", "Open or write a note first.")
            return

        tags = [tag.strip() for tag in self.tags_input.text().split(",") if tag.strip()]
        try:
            self.selected_note_id = self.manager.create_task(
                f"{title or 'Untitled note'} (Copy)",
                body,
                self.category_input.text(),
                tags,
                self.due_date_input.text().strip(),
            )
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

        result = QMessageBox.question(
            self,
            "Delete note",
            "Do you want to delete the selected note?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if result != QMessageBox.Yes:
            return

        current_row = self.notes_list.currentRow()
        target_row = max(0, current_row - 1)
        try:
            self.manager.remove_task(self.selected_note_id)
            self.selected_note_id = None
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
