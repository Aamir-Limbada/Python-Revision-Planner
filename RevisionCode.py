import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt


class RevisionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Revision Tracker")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #111318;
            }

            QWidget {
                color: #F1F1F5;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QLabel#pageTitle {
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#muted {
                color: #9699A8;
            }

            QFrame#sidebar {
                background-color: #191B23;
                border-right: 1px solid #2A2D38;
            }

            QPushButton {
                background-color: transparent;
                color: #B8BBC9;
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: left;
            }

            QPushButton:hover {
                background-color: #292C38;
                color: white;
            }

            QPushButton#activeNav {
                background-color: #6D5AE6;
                color: white;
                font-weight: 600;
            }

            QFrame#statCard {
                background-color: #191B23;
                border: 1px solid #2A2D38;
                border-radius: 12px;
            }

            QLabel#statValue {
                font-size: 28px;
                font-weight: 700;
            }

            QFrame#contentCard {
                background-color: #191B23;
                border: 1px solid #2A2D38;
                border-radius: 12px;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 20)
        sidebar_layout.setSpacing(8)

        logo = QLabel("Revision.")
        logo.setStyleSheet(
            "font-size: 23px; font-weight: 700; color: #9B8AFF;"
        )
        sidebar_layout.addWidget(logo)

        sidebar_layout.addSpacing(28)

        navigation_items = [
            ("Dashboard", True),
            ("My Topics", False),
            ("Revision History", False),
            ("Statistics", False),
        ]

        for name, active in navigation_items:
            button = QPushButton(name)

            if active:
                button.setObjectName("activeNav")

            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        settings_button = QPushButton("Settings")
        sidebar_layout.addWidget(settings_button)

        # Main content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(36, 30, 36, 30)
        content_layout.setSpacing(24)

        heading = QLabel("Dashboard")
        heading.setObjectName("pageTitle")

        subtitle = QLabel(
            "Track your progress and focus on what matters."
        )
        subtitle.setObjectName("muted")

        content_layout.addWidget(heading)
        content_layout.addWidget(subtitle)

        # Statistics cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        stats = [
            ("Topics", "0", "Topics created"),
            ("Revisions", "0", "Sessions completed"),
            ("Confidence", "—", "No data yet"),
        ]

        for title, value, description in stats:
            card = QFrame()
            card.setObjectName("statCard")
            card.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred,
            )

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(10)

            title_label = QLabel(title)
            title_label.setObjectName("muted")

            value_label = QLabel(value)
            value_label.setObjectName("statValue")

            description_label = QLabel(description)
            description_label.setObjectName("muted")

            card_layout.addWidget(title_label)
            card_layout.addWidget(value_label)
            card_layout.addWidget(description_label)

            stats_layout.addWidget(card)

        content_layout.addLayout(stats_layout)

        # Welcome panel
        welcome_card = QFrame()
        welcome_card.setObjectName("contentCard")

        welcome_layout = QVBoxLayout(welcome_card)
        welcome_layout.setContentsMargins(24, 24, 24, 24)
        welcome_layout.setSpacing(14)

        welcome_title = QLabel("Welcome to your revision space")
        welcome_title.setStyleSheet(
            "font-size: 20px; font-weight: 600;"
        )

        welcome_text = QLabel(
            "Create your first topic to start tracking your "
            "Computer Science revision, confidence and progress."
        )
        welcome_text.setObjectName("muted")
        welcome_text.setWordWrap(True)

        add_topic_button = QPushButton("+  Add your first topic")
        add_topic_button.setObjectName("activeNav")
        add_topic_button.setMaximumWidth(220)

        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addSpacing(8)
        welcome_layout.addWidget(add_topic_button)
        welcome_layout.addStretch()

        content_layout.addWidget(welcome_card, 1)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RevisionApp()
    window.show()

    sys.exit(app.exec())