from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from recipe_editor import RecipeEditor
import sqlite3
import sys
import os
# from config import DB_PATH

import shutil

def get_writable_db_path():
    # Use local app data for user-specific writable storage
    app_data_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'RecipeKeeper')
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, 'Recipe_keeper.db')

def get_bundled_db_path():
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, 'Recipe_keeper.db')

# Final DB path used by the app
db_path = get_writable_db_path()

# On first run, copy bundled DB to writable location
if not os.path.exists(db_path):
    try:
        shutil.copy2(get_bundled_db_path(), db_path)
    except Exception as e:
        raise RuntimeError(f"Failed to copy database: {e}")


class RecipeListWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Optional: store reference if needed
        self.list_widget = QListWidget
        conn = sqlite3.connect(get_writable_db_path())
        c = conn.cursor()
        c.execute("SELECT ID, RecipeName FROM Recipes WHERE visible = 1")
        results = c.fetchall()
        conn.close()

        for recipe_id, recipe_name in results:
            self.add_recipe_item(recipe_id, recipe_name) 


       

    def add_recipe_item(self, recipe_id, recipe_name):
        item = QListWidgetItem(recipe_name)
        item.setData(Qt.ItemDataRole.UserRole, recipe_id)
        # self.list_widget.addItem(item)
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("Recipe List")
        self.setWindowFlags(Qt.WindowType.Window)
        self.resize(575, 700)
        # self.load_recipes()

        self.recipe_list = QListWidget()
        main_layout.addWidget(self.recipe_list)
        conn = sqlite3.connect(get_writable_db_path())
        c = conn.cursor()
        c.execute("SELECT ID, RecipeName FROM Recipes WHERE visible = 1")
        results = c.fetchall()
        conn.close()

        for recipe in results:
            self.add_recipe_row(recipe)       

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.hide)
        main_layout.addWidget(close_btn)
        
    def add_recipe_row(self, recipe: tuple):
        recipe_id, recipe_name = recipe  
        row_widget = QWidget()   
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(6, 2, 6, 2)
        row_layout.setSpacing(10)

        id_label = QLabel(f"{recipe_id}")
        id_label.setStyleSheet("color: gray; font-weight: bold;")
        

        label = QLabel(recipe_name)
        label.setEnabled(True)
        label.setStyleSheet("color: black; font-weight: normal;")
        label.setFont(QFont("Arial", 13))
        metrics = QFontMetrics(label.font())
        # elided = metrics.elidedText(recipe, Qt.TextElideMode.ElideRight, 600)
        elided = metrics.elidedText(recipe[1], Qt.TextElideMode.ElideRight, 600)
        label.setText(elided)
        label.setMaximumWidth(600)
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        row_layout.addWidget(id_label)
        row_layout.addWidget(label)

        
        # Buttons
        view_button = QPushButton("View")
        recipe_id = recipe[0]  # or recipe[0] if it's a tuple
        view_button.setFixedSize(80, 30)
        view_button.setStyleSheet("background-color: #72b043; font-size:18px; font-weight:600;")
        
        view_button.clicked.connect(lambda _, rid=recipe_id: self.view_editor(rid))
        view_button.setToolTip(f"View recipe #{recipe_id}")
        # print(view_button.receivers(view_button.clicked))
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(80, 30)
        edit_button.setStyleSheet("background-color: #f8cc1b; font-size:18px; font-weight:600;")
        edit_button.clicked.connect(lambda _, r=recipe_id: self.edit_editor(r))

        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(80, 30)
        delete_button.setStyleSheet("background-color: #FF7276; font-size:18px; font-weight:600;")
        delete_button.clicked.connect(lambda _, r=recipe: self.delete_row_by_id(r[0]))


        row_layout.addStretch()
        row_layout.addWidget(view_button)
        row_layout.addWidget(edit_button)
        row_layout.addWidget(delete_button)

        item = QListWidgetItem()
        item.setSizeHint(row_widget.sizeHint())
        item.setData(Qt.ItemDataRole.UserRole, recipe_id)

        self.recipe_list.addItem(item)
        self.recipe_list.setItemWidget(item, row_widget)

    def view_editor(self, recipe_id: int):
                # First, ensure it's a string and check if it's a digit
            if isinstance(recipe_id, str):
                if recipe_id.strip().isdigit():
                    recipe_id = int(recipe_id.strip())
                    
                else:
                    QMessageBox.warning(self, "Invalid ID", "Recipe ID must be a number.")
                    return
        
                return
            
                # Now it's safe to use
            self.editor = RecipeEditor(recipe_id, mode="view")
            self.editor.show()


    def edit_editor(self, recipe_id: int):
                # First, ensure it's a string and check if it's a digit
            if isinstance(recipe_id, str):
                if recipe_id.strip().isdigit():
                    recipe_id = int(recipe_id.strip())
                else:
                    QMessageBox.warning(self, "Invalid ID", "Recipe ID must be a number.")
                    return
                return
            
                # Now it's safe to use
            self.editor = RecipeEditor(recipe_id, mode="edit")
            self.editor.show()


    def delete_row_by_id(self, recipe_id):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete recipe ID {recipe_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            print("Deletion cancelled.")
            return

        # print("Method ref:", self.delete_row_by_id)
        # print(f"Deleting recipe with ID: {recipe_id}")
        
        conn = sqlite3.connect(get_writable_db_path())
        c = conn.cursor()
        c.execute("UPDATE Recipes SET visible = 0 WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Deleted", f"Recipe {recipe_id} has been deleted.")
        self.close()



# app = QApplication([])
# window = RecipeListWindow()
# window.show()
# app.exec()
