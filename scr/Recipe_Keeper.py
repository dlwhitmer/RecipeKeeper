from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtPrintSupport import *
from converter import SecondWindow
import sqlite3

# utils.py
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)
db_path = resource_path("Recipe_keeper.db")
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database not found at {db_path}")


class RecipeKeeper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Test")
        self.resize(400, 300)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._is_dragging = False
        self._drag_start_position = QPoint()

        self.setWindowTitle("Recipe Keeper")
        self.setGeometry(350,75,900,700)
        self.setStyleSheet("background-color: #FDF6E3;")

        menu_bar = self.menuBar()
        self.setMenuBar(menu_bar)  # Might be optional, but clarifies intent

        #  Add menus to the menu bar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #2d2d2d;
                color: white;
                font: bold 14px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 15px;
            }
            QMenuBar::item:selected {
                background-color: #505050;
            }
            QMenu {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #2d2d2d;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #505050;
            }
        """)

        new_menu = menu_bar.addMenu("New")
        save_menu = menu_bar.addMenu("Save")
        list_menu = menu_bar.addMenu("List & Open")
        converter_menu = menu_bar.addMenu("Meas Conv")
        print_preview_menu = menu_bar.addMenu("Print Preview")

         # Add actions to the File menu
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_recipe)
        save_action = QAction("Save",self)
        save_action.triggered.connect(self.add_data)
        list_action = QAction("List Recipes",self)
        list_action.triggered.connect(self.list_recipes)
        converter_action = QAction("Converter",self)
        converter_action.triggered.connect(self.open_converter)
        print_preview_action = QAction("Print Preview",self)
        print_preview_action.triggered.connect(self.combine_texts)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)  # Close the app when Exit is clicked

        new_menu.addAction(new_action)
        new_menu.addAction(exit_action)
        save_menu.addAction(save_action)
        list_menu.addAction(list_action)
        converter_menu.addAction(converter_action)
        print_preview_menu.addAction(print_preview_action)

        title_layout = QHBoxLayout()
        self.title = QLabel("Recipe Keeper")
        self.title.setFixedSize(400,60)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.title,alignment=(Qt.AlignmentFlag.AlignCenter))
        self.title.setStyleSheet("font-family:'Century Schoolbook'; background-color: #E07A5F;font-size: 45px;color: #3D3D3D; font-weight: 700px; border: 5px outset #00202e; border-radius: 20px;")

        recipe_name_layout = QHBoxLayout()
        self.Recipe_Name = QTextEdit(self)
        self.Recipe_Name.setFixedSize(350,50)
        self.Recipe_Name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        recipe_name_layout.addWidget(self.Recipe_Name, alignment=(Qt.AlignmentFlag.AlignCenter))
        self.Recipe_Name.setStyleSheet("background-color: #E07A5F;font-family:'Goudy Old Style';font-size: 25px; font-weight:600;border: 4px solid  #00202e; border-radius: 25px;")

        label_layout = QHBoxLayout()
        self.Ingredients_label = QLabel("Ingredients")
        label_layout.addWidget(self.Ingredients_label)
        self.Ingredients_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Ingredients_label.setFixedSize(250, 45)  # Keep this if needed
        self.Ingredients_label.setMargin(0)           # Try reducing margin first
        self.Ingredients_label.setStyleSheet("""
        QLabel {
        background-color: #E07A5F;
        border: 2px solid black;  /* Border width and color */
        border-radius: 20px;      /* Rounded corners (optional) */
        font-size: 25px;
        color:#3D3D3D;
        font-weight: 600;
            }
        """)

        self.Instructions_label = QLabel("Instructions")
        label_layout.addWidget(self.Instructions_label)
        self.Instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Instructions_label.setFixedSize(250, 45)  # Keep this if needed
        self.Instructions_label.setMargin(0)           # Try reducing margin first
        self.Instructions_label.setStyleSheet("""
    QLabel {
        background-color: #E07A5F;
        border: 2px solid black;  /* Border width and color */
        border-radius: 20px;      /* Rounded corners (optional) */
        font-size: 25px;
        color:#3D3D3D;
        font-weight: 600;
    }
""")
        ing_inst_layout = QHBoxLayout()
        self.Ingredients = QTextEdit()
        self.Ingredients.setFixedSize(450,400)
        self.Ingredients.setStyleSheet(" background-color: #81B29A; font-family:'Goudy Old Style';border: 2px solid #000; border-radius: 25px; font-size: 20px; font-weight: 600")
        ing_inst_layout.addWidget(self.Ingredients,alignment=(Qt.AlignmentFlag.AlignLeft))

        self.Instructions = QTextEdit()
        self.Instructions.setFixedSize(450,400)
        self.Instructions.setStyleSheet(" background-color: #81B29A; font-family:'Goudy Old Style'; border: 2px solid #000; border-radius: 25px; font-size: 20px; font-weight: 600")
        ing_inst_layout.addWidget(self.Instructions, alignment=(Qt.AlignmentFlag.AlignRight))
        space_layout = QHBoxLayout()
        self.space = QTextEdit()
        self.space.setFixedSize(900,50)
        space_layout.addWidget(self.space)
        self.space.setStyleSheet("background-color: transparent;border: none;")

        label2_layout = QHBoxLayout()
        self.label_7 = QLabel(self)  
        label2_layout.addWidget(self.label_7)
        labfont = QFont("Times New Roman", 14)
        labfont.setBold(True)
        self.label_7.setFont(labfont)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_7.setFixedSize(200,50)
        self.label_7.move(350, 200)  
        self.label_7.setVisible(False)
        self.label_7.setStyleSheet("""
                QLabel{
                    background-color: #E07A5F;
                    color: #3D3D3D;  
                    border: 3px solid black;
                    border-radius: 15px;
                }
""")
        
        self.combo_list = QComboBox()
        self.combo_list.setWindowTitle("Recipe List")
        # layout.addWidget(self.combo_list)
        self.combo_list.clear()  # Ensure it's fresh
        self.combo_list.addItem("Click on Recipe to Open it:")  # Add your placeholder
        self.combo_list.setCurrentIndex(0)  # Preselect the placeholder

        # Disable placeholder (after adding it)
        index = self.combo_list.findText("Click on Recipe to Open it:")
        if index >= 0:
               item = self.combo_list.model().item(index)
        if item:
               item.setEnabled(False)

        self.load_recipes_into_combo()  # Now add the actual recipes
        self.combo_list.setMinimumWidth(300)  # Optional: Set a nice minimum width
        self.setMinimumHeight(50)
        lwfont = QFont("Times New Roman",14)
        lwfont.setBold(True)
        self.combo_list.setFont(lwfont)
        self.combo_list.move(600,300)
        self.combo_list.currentTextChanged.connect(self.get_input)
        self.combo_list.setStyleSheet("""
    QComboBox {
        background-color: #fbf2c4;  /* Light gray background */
        border: 1px solid #d3d3d3; /* Light border */
        font-size: 17px;
        font-weight: 700;
        padding: 5px;
    }
    QComboBox::item {
        padding: 10px;             /* Add padding to items */
        color: #000000;            /* Text color */
    }
    QComboBox::item:hover {
        background-color: #cce7ff; /* Light blue hover effect */
    }
    QComboBox::item:selected {
        background-color: #3399ff; /* Blue selection background */
        color: white;              /* White text for selected item */
    }
""")


        main_layout.addLayout(title_layout)
        main_layout.addLayout(recipe_name_layout)
        main_layout.addLayout(label_layout)
        main_layout.addLayout(ing_inst_layout)
        main_layout.addLayout(space_layout)
        main_layout.addLayout(label2_layout)

    def new_recipe(self):
         self.Recipe_Name.clear()   
         self.Ingredients.clear()   
         self.Instructions.clear()

    def add_data(self):
        if self.Recipe_Name.toPlainText().strip() == "":
             QMessageBox.information(
            self,
            'Information',
            'Recipe Name Cannot be Empty'
        )
        elif self.Ingredients.toPlainText().strip() == "":
                  QMessageBox.information(
                       self,
                        'Information',
                        'Ingredients Cannot be Empty'
        )       
        elif self.Instructions.toPlainText().strip() == "":
                  QMessageBox.information(
                       self,
                        'Information',
                        'Instructions Cannot be Empty'
        )
        else:
              self.RecipeName = self.Recipe_Name.toPlainText()
              self.ingredient = self.Ingredients.toPlainText()
              self.instructions = self.Instructions.toPlainText()
              conn = sqlite3.connect(db_path)
              c = conn.cursor()
              c.execute('INSERT INTO Recipes (RecipeName, Ingredients, Instructions) \
                  VALUES (?,?,?)',(self.RecipeName, self.ingredient, self.instructions))
              conn.commit()
              conn.close()
              self.label_7.setVisible(True)
              self.label_7.setText('Recipe Added!')
              if self.RecipeName and self.Recipe_Name not in [self.combo_list.itemText(i) for i in range(self.combo_list.count())]:
                   self.combo_list.addItem(self.RecipeName)


    def get_input(self, selected_text=None):
         self.combo_list.setVisible(False)
         self.user_input = self.combo_list.currentText()
         print(self.user_input)
         conn = sqlite3.connect(db_path)
         c = conn.cursor()
         query = "SELECT * FROM Recipes WHERE RecipeName = ?"
         c.execute(query, (self.user_input,))
         result = c.fetchone()
         conn.close()

         if result:
              self.Recipe_Name.setText(f"{result[1]}")
              self.Ingredients.setText(f"{result[2]}")
              self.Instructions.setText(f"{result[3]}")
         else:
              self.Recipe_Name.setText("No recipe found with that name.")

    def load_recipes_into_combo(self):
         conn = sqlite3.connect(db_path)
         c = conn.cursor()
         c.execute("SELECT RecipeName FROM Recipes")
         recipes = c.fetchall()
         conn.close()
         # Only add recipes that aren’t already in the box
         existing_items = {self.combo_list.itemText(i) for i in range(self.combo_list.count())}
         for name_tuple in recipes:
            recipe_name = name_tuple[0]
            if recipe_name not in existing_items:
                self.combo_list.addItem(recipe_name)

    def list_recipes(self):
         self.combo_list.setVisible(True)

    def open_converter(self):
        # Create and show the second page
        self.sec_win = SecondWindow()
        self.sec_win.show() 

    def combine_texts(self):
        self.text1 = self.Recipe_Name.toPlainText()
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





    

app = QApplication([])
window = RecipeKeeper()
window.show()
app.exec()