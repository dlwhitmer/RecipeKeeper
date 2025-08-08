import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import *
from typing import Optional
from db_utils import soft_delete_recipe
import sqlite3
import os

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


class RecipeEditor(QMainWindow):
    def __init__(self, recipe_id: str = None, mode: str = "view"):
        super().__init__()
        self.recipe_id = recipe_id
        self.mode = mode
       
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Editor")
        self.setGeometry(100,100,800,500)
        self.setStyleSheet("background-color:#cbd8df;")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._is_dragging = False
        self._drag_start_position = QPoint()

        name_layout = QHBoxLayout()
        self.id = QLineEdit()
        self.id.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id.setFixedSize(50,40)
        self.id.setStyleSheet("background-color:#fbf2c4; border: 2px solid #000; border-radius: 15px;")
        self.id_lbl = QLabel("Recipe Id")
        self.id_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_lbl.setFixedWidth(100)
        self.id_lbl.setStyleSheet("font-size: 20px; font-weight: 600;")
        self.RecipeName = QLineEdit()
        self.recipe_name_lbl = QLabel("Recipe Name")
        self.recipe_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recipe_name_lbl.setFixedWidth(120)
        self.recipe_name_lbl.setStyleSheet("font-size: 20px; font-weight: 600;")
        name_layout.addWidget(self.id_lbl)
        name_layout.addWidget(self.id)
        name_layout.addWidget(self.recipe_name_lbl)
        name_layout.addWidget(self.RecipeName)
        name_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RecipeName.setFixedSize(400,40)
        self.RecipeName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RecipeName.setStyleSheet("font-size: 20px; font-weight:600; background-color:#fbf2c4; border: 2px solid #000; border-radius: 15px;")

        label_layout = QHBoxLayout()
        self.ing_label = QLabel("Ingredients")
        self.ing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ing_label.setStyleSheet("background-color:#fbf2c4; font-size: 20px; font-weight: 600; ")
        self.inst_label = QLabel("Instructions")
        self.inst_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inst_label.setStyleSheet("background-color:#fbf2c4; font-size: 20px; font-weight: 600; ")
        label_layout.addWidget(self.ing_label)
        label_layout.addWidget(self.inst_label)

        info_label = QHBoxLayout()
        self.Ingredients = QTextEdit()
        self.Ingredients.setStyleSheet("background-color:#fff6ea; font-size: 20px; font-weight: 600; ")
        self.Instructions = QTextEdit()
        self.Instructions.setStyleSheet("background-color:#fff6ea; font-size: 20px; font-weight: 600; ")
        info_label.addWidget(self.Ingredients)
        info_label.addWidget(self.Instructions)

        btn_layout = QHBoxLayout()
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedSize(100,40)
        self.close_btn.setStyleSheet("background-color:#fbf2c4; text-align: center; font-size:20px; font-weight:600;")
        self.close_btn
        self.close_btn.clicked.connect(self.close)
        self.update_btn = QPushButton("Update")
        self.update_btn.setFixedSize(100,40)
        self.update_btn.setStyleSheet("color: #000;background-color:#fbf2c4; text-align: center; font-size:20px; font-weight:600;")
        self.update_btn.clicked.connect(self.update_recipe)
        self.print_preview_btn = QPushButton("Print Preview")
        self.print_preview_btn.setFixedSize(150,40)
        self.print_preview_btn.setStyleSheet("background-color:#fbf2c4; text-align: center; font-size:20px; font-weight:600;")
        self.print_preview_btn.clicked.connect(self.combine_texts)
        btn_layout.addWidget(self.close_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.print_preview_btn)


        layout.addLayout(name_layout)
        layout.addLayout(label_layout)
        layout.addLayout(info_label)
        layout.addLayout(btn_layout)

        if self.mode == "view":
            self.enable_viewing()
        if self.mode == "edit":
            self.enable_editing()
            
        elif self.mode == "delete":
            self.delete_row_by_id(self.recipe_id)

    def enable_viewing(self):
        self.update_btn.hide()
        self.id.setReadOnly(True)
        self.RecipeName.setReadOnly(True)
        self.Ingredients.setReadOnly(True)
        self.Instructions.setReadOnly(True)
        self.update_btn.setEnabled(False)  # Disable update/save
        self.load_recipe(self.recipe_id)


    def enable_editing(self):
        self.update_btn.show()
        self.id.setReadOnly(True)  # Usually you don't want to edit the ID
        self.RecipeName.setReadOnly(False)
        self.Ingredients.setReadOnly(False)
        self.Instructions.setReadOnly(False)
        self.update_btn.setEnabled(True)
        self.load_recipe(self.recipe_id)
    
    def prepare_for_delete(self):
        self.update_btn.hide()
        self.id.setReadOnly(True)  # Usually you don't want to edit the ID
        self.RecipeName.setReadOnly(False)
        self.Ingredients.setReadOnly(False)
        self.Instructions.setReadOnly(False)
        # self.update_btn.setEnabled(True)


    def combine_texts(self):
        self.text1 = self.RecipeName.text()
        self.text2 = self.Ingredients.toPlainText()
        self.text3 = self.Instructions.toPlainText()
        # Combine the texts
        self.Recipe = f"{self.text1}\n{self.text2}\n{self.text3}" 
        self.show_print_preview() 

    def show_print_preview(self):
        self.printer = QPrinter()
        preview_dialog = QPrintPreviewDialog(self.printer, self)
        preview_dialog.paintRequested.connect(self.print_preview)
        preview_dialog.exec()    

    def print_preview(self, printer):
        # Render the string using QTextDocument
        self.document = QTextDocument()
        self.document.setPlainText(self.Recipe)
        font = QFont("Times New Roman",15)
        font.setBold(True)
        self.document.setDefaultFont(font)
        self.document.print(printer)

    def load_all_recipes(self, only_visible=True):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            query = "SELECT ID, RecipeName FROM Recipes"
            if only_visible:
                query += " WHERE visible = 1"
            c.execute(query)
            return c.fetchall()



    def load_recipe(self, recipe_id: int):
      
        conn = sqlite3.connect(get_writable_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT ID, RecipeName, Ingredients, Instructions 
            FROM Recipes 
            WHERE ID = ? AND visible = 1
        """, (recipe_id,))
        row = c.fetchone()
        conn.close()

        font = QFont("Arial", 16)
        font.setBold(True)

        if row:
            self.id.setText(str(row[0]))
            self.id.setFont(font)
            self.RecipeName.setText(row[1])
            self.RecipeName.setFont(font)
            self.Ingredients.setPlainText(row[2])
            self.Ingredients.setFont(font)
            self.Instructions.setPlainText(row[3])
            self.Instructions.setFont(font)
        else:
            self.RecipeName.setText("No visible recipe found with that ID.")



    def update_recipe(self):
        recipe_id = self.id.text()
        recipe_name = self.RecipeName.text()
        recipe_ingredients = self.Ingredients.toPlainText()
        recipe_instructions = self.Instructions.toPlainText()
        if not self.id.text().isdigit() or not recipe_name or not recipe_ingredients or not recipe_instructions:
            QMessageBox.warning(self, "Error", "All fields must be filled out.")
            return
        conn = sqlite3.connect(get_writable_db_path())
        c = conn.cursor()
        c.execute(
             "UPDATE Recipes SET RecipeName = ?, Ingredients = ?, Instructions = ?, visible = ? WHERE id = ?",
                (recipe_name, recipe_ingredients, recipe_instructions, 1, recipe_id)
            )
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Recipe updated successfully!")

    def delete_row_by_id(self, recipe_id):
        soft_delete_recipe(db_path, recipe_id)
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

        print("Method ref:", self.delete_row_by_id)
        print(f"Deleting recipe with ID: {recipe_id}")
        conn = sqlite3.connect(get_writable_db_path())
        cursor = conn.cursor()
        cursor.execute("UPDATE Recipes SET visible = 0 WHERE id = ?", (recipe_id,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Deleted", f"Recipe {recipe_id} has been deleted.")
        self.close()


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = False
            event.accept()


       

# app = QApplication([])
# window = RecipeEditor()
# window.show()
# app.exec()