from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import pyqtSignal

class RecipeItemWidget(QWidget):
    # Emit recipe ID when user clicks edit or delete
    editRequested = pyqtSignal(int)
    deleteRequested = pyqtSignal(int)
    openRequested = pyqtSignal(int)

    def __init__(self, recipe_id, title, thumbnail_path=None, parent=None):
        super().__init__(parent)
        self.recipe_id = recipe_id
        self.title = title
        self.thumbnail_path = thumbnail_path

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        # Thumbnail
        if self.thumbnail_path:
            pixmap = QPixmap(self.thumbnail_path).scaled(64, 64)
            self.thumb_label = QLabel()
            self.thumb_label.setPixmap(pixmap)
        else:
            self.thumb_label = QLabel("🥣")

        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

        # Buttons
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(lambda: self.editRequested.emit(self.recipe_id))

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(lambda: self.deleteRequested.emit(self.recipe_id))

        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(lambda: self.openRequested.emit(self.recipe_id))

        # Layouts
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.title_label)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        text_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.thumb_label)
        main_layout.addLayout(text_layout)
        self.setLayout(main_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e2e2e2;
                border-radius: 8px;
                padding: 8px;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #cccccc;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #aaaaaa;
            }
        """)
