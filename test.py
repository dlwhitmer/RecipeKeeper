from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a menu bar
        menu_bar = self.menuBar()

        # Add menus to the menu bar
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")

        # Add actions to the File menu
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)  # Close the app when Exit is clicked

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()  # Add a separator line
        file_menu.addAction(exit_action)

        # Add actions to the Edit menu
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)

        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # Set the window title and size
        self.setWindowTitle("PyQt6 Menu Bar Example")
        self.resize(400, 300)

# Run the application
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
