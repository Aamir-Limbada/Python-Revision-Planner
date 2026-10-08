
import sys
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QMessageBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)


APP_STYLE = """
QMainWindow, QWidget#page {
    background-color: #11131A;
    color: #F1F1F7;
    font-family: "Segoe UI";
    font-size: 14px;
}

QLabel {
    color: #F1F1F7;
}

QLabel#pageTitle {
    font-size: 28px;
    font-weight: 700;
}

QLabel#subtitle, QLabel#muted {
    color: #999DAF;
}

QLabel#brand {
    font-size: 25px;
    font-weight: 800;
    color: #A99AFF;
}

QLabel#sectionTitle {
    font-size: 19px;
    font-weight: 650;
}

QFrame#sidebar {
    background-color: #191B25;
    border-right: 1px solid #292C38;
}

QPushButton {
    background-color: transparent;
    color: #B9BDCC;
    border: none;
    border-radius: 8px;
    padding: 11px 13px;
    text-align: left;
}

QPushButton:hover {
    background-color: #292C3A;
    color: white;
}

QPushButton#activeNav {
    background-color: #6E5AE8;
    color: white;
    font-weight: 600;
}

QPushButton#primary {
    background-color: #7562F0;
    color: white;
    font-weight: 600;
    padding: 12px 16px;
}

QPushButton#primary:hover {
    background-color: #8775FF;
}

QPushButton#secondary {
    border: 1px solid #393D4C;
    background-color: #20232E;
    color: #E4E5ED;
}

QPushButton#danger {
    color: #FF999F;
    border: 1px solid #59343C;
}

QFrame#card {
    background-color: #191C26;
    border: 1px solid #2B2F3D;
    border-radius: 12px;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #1C1F2A;
    border: 1px solid #383C4D;
    border-radius: 7px;
    padding: 9px;
    color: #F1F1F7;
    min-height: 20px;
}

QComboBox QAbstractItemView {
    background-color: #1C1F2A;
    color: #F1F1F7;
    selection-background-color: #6E5AE8;
}

QTableWidget {
    background-color: #191C26;
    alternate-background-color: #1E212C;
    color: #F1F1F7;
    border: 1px solid #2B2F3D;
    border-radius: 10px;
    gridline-color: #2B2F3D;
    selection-background-color: #39315F;
    selection-color: white;
}

QHeaderView::section {
    background-color: #20232E;
    color: #BFC2D1;
    border: none;
    border-bottom: 1px solid #343847;
    padding: 12px;
    font-weight: 600;
}

QDialog {
    background-color: #141620;
}

QMessageBox {
    background-color: #191C26;
}

QScrollBar:vertical {
    background: #151720;
    width: 9px;
}

QScrollBar::handle:vertical {
    background: #41455A;
    border-radius: 4px;
    min-height: 25px;
}
"""


class AddTopicDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add a topic")
        self.setMinimumWidth(390)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Create a topic")
        title.setObjectName("sectionTitle")

        subtitle = QLabel(
            "Start tracking an area of your Computer Science revision."
        )
        subtitle.setObjectName("muted")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        form = QFormLayout()
        form.setSpacing(12)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Binary Search")

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems([
            "Algorithms",
            "Programming",
            "Data Structures",
            "Computer Systems",
            "Networks",
            "Databases",
            "Cyber Security",
            "Other",
        ])
        self.category_input.setCurrentText("Algorithms")

        self.confidence_input = QSpinBox()
        self.confidence_input.setRange(1, 5)
        self.confidence_input.setValue(3)
        self.confidence_input.setSuffix(" / 5")

        form.addRow("Topic name", self.name_input)
        form.addRow("Category", self.category_input)
        form.addRow("Starting confidence", self.confidence_input)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("secondary")
        cancel_button.clicked.connect(self.reject)

        create_button = QPushButton("Create topic")
        create_button.setObjectName("primary")
        create_button.clicked.connect(self.validate_and_accept)

        buttons.addWidget(cancel_button)
        buttons.addWidget(create_button)

        layout.addLayout(buttons)

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(
                self,
                "Missing topic name",
                "Please enter a name for your topic.",
            )
            self.name_input.setFocus()
            return

        if not self.category_input.currentText().strip():
            QMessageBox.warning(
                self,
                "Missing category",
                "Please enter or select a category.",
            )
            return

        self.accept()

    def get_topic_data(self):
        return {
            "name": self.name_input.text().strip(),
            "category": self.category_input.currentText().strip(),
            "confidence": self.confidence_input.value(),
            "sessions": [],
            "created": datetime.now().strftime("%d %b %Y"),
        }


class RevisionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ByteBack | CS Revision")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 760)

        # Temporary storage. SQLite will replace this later.
        self.topics = []
        self.current_page = 0

        self.setStyleSheet(APP_STYLE)
        self.setup_ui()
        self.show_page(0)

    def setup_ui(self):
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.setCentralWidget(root)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(225)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 25, 16, 20)
        sidebar_layout.setSpacing(7)

        brand = QLabel("ByteBack.")
        brand.setObjectName("brand")

        tagline = QLabel("YOUR CS REVISION SPACE")
        tagline.setObjectName("muted")
        tagline.setStyleSheet("font-size: 10px; letter-spacing: 1px;")

        sidebar_layout.addWidget(brand)
        sidebar_layout.addWidget(tagline)
        sidebar_layout.addSpacing(30)

        self.nav_buttons = []

        nav_items = [
            ("⌂   Dashboard", 0),
            ("▤   My Topics", 1),
            ("◷   Revision History", 2),
            ("▥   Statistics", 3),
        ]

        for label, page_index in nav_items:
            button = QPushButton(label)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, index=page_index:
                self.show_page(index)
            )
            self.nav_buttons.append(button)
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        settings_button = QPushButton("⚙   Settings & About")
        settings_button.clicked.connect(
            lambda: self.show_page(4)
        )
        sidebar_layout.addWidget(settings_button)

        sidebar_layout.addSpacing(10)

        footer = QLabel("Small steps. Stronger knowledge.")
        footer.setObjectName("muted")
        footer.setWordWrap(True)
        footer.setStyleSheet("font-size: 11px;")
        sidebar_layout.addWidget(footer)

        # Pages
        self.pages = QStackedWidget()

        self.dashboard_page = self.build_dashboard()
        self.topics_page = self.build_topics_page()
        self.history_page = self.build_history_page()
        self.statistics_page = self.build_statistics_page()
        self.settings_page = self.build_settings_page()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.topics_page)
        self.pages.addWidget(self.history_page)
        self.pages.addWidget(self.statistics_page)
        self.pages.addWidget(self.settings_page)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.pages, 1)

    def create_page(self, title, subtitle):
        page = QWidget()
        page.setObjectName("page")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(22)

        heading = QLabel(title)
        heading.setObjectName("pageTitle")

        description = QLabel(subtitle)
        description.setObjectName("subtitle")
        description.setWordWrap(True)

        layout.addWidget(heading)
        layout.addWidget(description)

        return page, layout

    def create_card(self):
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(9)

        return card, layout

    def build_dashboard(self):
        page, layout = self.create_page(
            "Your dashboard",
            "Your progress, your pace. Let's see where you stand."
        )

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)

        self.topic_count_label = QLabel("0")
        self.session_count_label = QLabel("0")
        self.confidence_label = QLabel("—")

        for title, value_label, detail in [
            ("TOPICS TRACKED", self.topic_count_label, "Areas you're studying"),
            ("SESSIONS LOGGED", self.session_count_label, "Revision sessions"),
            ("AVG. CONFIDENCE", self.confidence_label, "Across your topics"),
        ]:
            card, card_layout = self.create_card()

            heading = QLabel(title)
            heading.setObjectName("muted")
            heading.setStyleSheet("font-size: 11px; font-weight: 600;")

            value_label.setStyleSheet(
                "font-size: 30px; font-weight: 700; color: #B2A5FF;"
            )

            detail_label = QLabel(detail)
            detail_label.setObjectName("muted")

            card_layout.addWidget(heading)
            card_layout.addWidget(value_label)
            card_layout.addWidget(detail_label)

            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        welcome_card, welcome_layout = self.create_card()

        welcome_title = QLabel("Build your revision space")
        welcome_title.setObjectName("sectionTitle")

        welcome_text = QLabel(
            "Add the Computer Science topics you're studying. "
            "ByteBack will help you track confidence and, once you "
            "start logging sessions, identify areas that need attention."
        )
        welcome_text.setObjectName("muted")
        welcome_text.setWordWrap(True)

        self.dashboard_topic_button = QPushButton("+   Add a topic")
        self.dashboard_topic_button.setObjectName("primary")
        self.dashboard_topic_button.setMaximumWidth(180)
        self.dashboard_topic_button.clicked.connect(self.add_topic)

        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addSpacing(8)
        welcome_layout.addWidget(self.dashboard_topic_button)
        welcome_layout.addStretch()

        layout.addWidget(welcome_card, 1)

        self.recent_title = QLabel("Your topics")
        self.recent_title.setObjectName("sectionTitle")
        layout.addWidget(self.recent_title)

        self.dashboard_topic_list = QLabel(
            "No topics yet. Add your first one to get started."
        )
        self.dashboard_topic_list.setObjectName("muted")
        self.dashboard_topic_list.setWordWrap(True)
        layout.addWidget(self.dashboard_topic_list)

        return page

    def build_topics_page(self):
        page, layout = self.create_page(
            "My topics",
            "Create and manage the areas you want to improve."
        )

        toolbar = QHBoxLayout()

        toolbar.addStretch()

        add_button = QPushButton("+   Add topic")
        add_button.setObjectName("primary")
        add_button.clicked.connect(self.add_topic)

        delete_button = QPushButton("Delete selected")
        delete_button.setObjectName("danger")
        delete_button.clicked.connect(self.delete_topic)

        toolbar.addWidget(delete_button)
        toolbar.addWidget(add_button)

        layout.addLayout(toolbar)

        self.topic_table = QTableWidget(0, 3)
        self.topic_table.setHorizontalHeaderLabels([
            "Topic", "Category", "Confidence"
        ])
        self.topic_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.topic_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.topic_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.topic_table.setAlternatingRowColors(True)
        self.topic_table.verticalHeader().setVisible(False)
        self.topic_table.verticalHeader().setDefaultSectionSize(48)

        header = self.topic_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        header.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )

        layout.addWidget(self.topic_table, 1)

        self.topics_empty_label = QLabel(
            "Your topic list is empty. Select '+ Add topic' to begin."
        )
        self.topics_empty_label.setObjectName("muted")
        self.topics_empty_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(self.topics_empty_label)

        return page

    def build_history_page(self):
        page, layout = self.create_page(
            "Revision history",
            "A record of the work you've put in."
        )

        card, card_layout = self.create_card()

        self.history_message = QLabel(
            "No revision sessions yet.\n\n"
            "Once we add the revision-session feature, "
            "your completed sessions will appear here."
        )
        self.history_message.setObjectName("muted")
        self.history_message.setWordWrap(True)

        card_layout.addWidget(self.history_message)
        layout.addWidget(card)
        layout.addStretch()

        return page

    def build_statistics_page(self):
        page, layout = self.create_page(
            "Statistics",
            "A clearer picture of your progress."
        )

        card, card_layout = self.create_card()

        self.statistics_message = QLabel("")
        self.statistics_message.setWordWrap(True)

        card_layout.addWidget(self.statistics_message)
        layout.addWidget(card)
        layout.addStretch()

        return page

    def build_settings_page(self):
        page, layout = self.create_page(
            "Settings & About",
            "A few details about your revision workspace."
        )

        card, card_layout = self.create_card()

        app_name = QLabel("ByteBack")
        app_name.setObjectName("sectionTitle")

        description = QLabel(
            "A personal Computer Science revision tracker built "
            "with Python and PySide6."
        )
        description.setObjectName("muted")
        description.setWordWrap(True)

        version = QLabel("Version 0.1.0 — Early development")

        note = QLabel(
            "Your topics are currently stored in memory and will "
            "reset when you close the application. Persistent "
            "storage will be added with SQLite."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #D6B66C;")

        card_layout.addWidget(app_name)
        card_layout.addWidget(description)
        card_layout.addWidget(version)
        card_layout.addWidget(note)

        layout.addWidget(card)
        layout.addStretch()

        return page

    def show_page(self, index):
        self.current_page = index
        self.pages.setCurrentIndex(index)

        for button_index, button in enumerate(self.nav_buttons):
            button.setObjectName(
                "activeNav" if button_index == index else ""
            )
            button.style().unpolish(button)
            button.style().polish(button)

        self.refresh_ui()

    def add_topic(self):
        dialog = AddTopicDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        topic = dialog.get_topic_data()

        duplicate = any(
            existing["name"].casefold() == topic["name"].casefold()
            for existing in self.topics
        )

        if duplicate:
            QMessageBox.warning(
                self,
                "Topic already exists",
                "You've already created a topic with that name.",
            )
            return

        self.topics.append(topic)
        self.refresh_ui()

        QMessageBox.information(
            self,
            "Topic created",
            f'"{topic["name"]}" has been added to your topics.',
        )

    def delete_topic(self):
        selected_row = self.topic_table.currentRow()

        if selected_row < 0:
            QMessageBox.information(
                self,
                "No topic selected",
                "Select a topic from the table first.",
            )
            return

        topic_name = self.topics[selected_row]["name"]

        answer = QMessageBox.question(
            self,
            "Delete topic",
            f'Delete "{topic_name}" and its recorded sessions?',
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.topics.pop(selected_row)
            self.refresh_ui()

    def refresh_ui(self):
        total_topics = len(self.topics)

        total_sessions = sum(
            len(topic["sessions"]) for topic in self.topics
        )

        if total_topics:
            average_confidence = sum(
                topic["confidence"] for topic in self.topics
            ) / total_topics
            self.confidence_label.setText(
                f"{average_confidence:.1f}/5"
            )
        else:
            self.confidence_label.setText("—")

        self.topic_count_label.setText(str(total_topics))
        self.session_count_label.setText(str(total_sessions))

        self.topic_table.setRowCount(total_topics)

        for row, topic in enumerate(self.topics):
            name_item = QTableWidgetItem(topic["name"])
            category_item = QTableWidgetItem(topic["category"])
            confidence_item = QTableWidgetItem(
                f'{topic["confidence"]}/5'
            )

            confidence_item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.topic_table.setItem(row, 0, name_item)
            self.topic_table.setItem(row, 1, category_item)
            self.topic_table.setItem(row, 2, confidence_item)

        self.topics_empty_label.setVisible(total_topics == 0)
        self.topic_table.setVisible(total_topics > 0)

        self.dashboard_topic_button.setVisible(total_topics == 0)
        self.recent_title.setVisible(total_topics > 0)
        self.dashboard_topic_list.setVisible(total_topics > 0)

        if total_topics:
            lines = []

            for topic in self.topics[:5]:
                confidence = topic["confidence"]
                lines.append(
                    f'•  {topic["name"]}  —  '
                    f'{topic["category"]}  —  '
                    f'Confidence {confidence}/5'
                )

            if total_topics > 5:
                lines.append(
                    f"...and {total_topics - 5} more topics."
                )

            self.dashboard_topic_list.setText("\n".join(lines))

        self.history_message.setText(
            f"You have completed {total_sessions} revision "
            f"session(s) across {total_topics} topic(s).\n\n"
            "The detailed session history will appear here "
            "once we build revision logging."
            if total_sessions
            else
            "No revision sessions yet.\n\n"
            "Once we add the revision-session feature, "
            "your completed sessions will appear here."
        )

        if total_topics:
            lowest = min(
                self.topics,
                key=lambda topic: topic["confidence"]
            )

            self.statistics_message.setText(
                f"Topics tracked: {total_topics}\n\n"
                f"Sessions recorded: {total_sessions}\n\n"
                f"Average confidence: "
                f"{self.confidence_label.text()}\n\n"
                f"Lowest-confidence topic: {lowest['name']} "
                f"({lowest['confidence']}/5)\n\n"
                "These figures will become more informative "
                "when revision results and history are available."
            )
        else:
            self.statistics_message.setText(
                "No statistics yet.\n\n"
                "Create some topics to start building your "
                "revision overview."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("ByteBack")

    window = RevisionApp()
    window.show()

    sys.exit(app.exec())