from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtPrintSupport import *
from recipe_list_window import RecipeListWindow
from converter import SecondWindow
import sqlite3
import os
import sys
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
print("sys.argv[0]:", sys.argv[0])
print("__file__:", __file__)




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

        new_menu = menu_bar.addMenu("New Recipe")
        save_menu = menu_bar.addMenu("Save Recipe")
        list_menu = menu_bar.addMenu("My Recipes")
        tools_menu = menu_bar.addMenu("Tools")
        
        tools_menu.setToolTip("Convert between grams/ounces and Celsius/Fahrenheit")

         # Add actions to the File menu
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_recipe)
        save_action = QAction("Save Recipe",self)
        save_action.triggered.connect(self.add_data)
        list_action = QAction("List Recipes",self)
        list_action.triggered.connect(self.launch_list_window)
        tools_menu.addAction("Unit Converter")
        tools_menu.triggered.connect(self.open_converter)
        
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)  # Close the app when Exit is clicked

        new_menu.addAction(new_action)
        new_menu.addAction(exit_action)
        save_menu.addAction(save_action)
        list_menu.addAction(list_action)
        tools_menu.setToolTip("Convert between grams/ounces and Celsius/Fahrenheit")


        self.title = QLabel("Recipe Keeper")
        self.title.setFixedSize(400,60)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-family:'Century Schoolbook'; background-color: #E07A5F;font-size: 45px;color: #3D3D3D; font-weight: 700px; border: 5px outset #00202e; border-radius: 20px;")

        title_layout_container = QWidget()

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0,0,0,0)
        title_layout.addWidget(self.title)
        title_layout_container.setLayout(title_layout)
        title_layout_container.setFixedHeight(60)  # or whatever height fits your design
        # title_layout_container.setStyleSheet("border: 2px dashed red; background-color: rgba(255, 0, 0, 30);")

        self.Recipe_Name = QTextEdit()
        self.Recipe_Name.setFixedSize(350,50)
        self.Recipe_Name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # recipe_name_layout_container.addWidget(self.Recipe_Name, alignment=(Qt.AlignmentFlag.AlignCenter))
        self.Recipe_Name.setStyleSheet("background-color: #E07A5F;font-family:'Arial';font-size: 25px; font-weight:600; border: 4px solid  #00202e; border-radius:25px;")

        recipe_name_layout_container = QWidget()

        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0,0,0,0)
        container_layout.addWidget(self.Recipe_Name)
        recipe_name_layout_container.setLayout(container_layout)
        recipe_name_layout_container.setFixedHeight(60)  # or whatever height fits your design
        # recipe_name_layout_container.setStyleSheet("border: 2px dashed red; background-color: rgba(255, 0, 0, 30);")

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

        self.label_7 = QLabel(self)  
        labfont = QFont("Times New Roman", 14)
        labfont.setBold(True)
        self.label_7.setFont(labfont)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_7.setFixedSize(200,50)
        # self.label_7.move(350, 200)  
        self.label_7.setVisible(False)
        self.label_7.setStyleSheet("""
                QLabel{
                    background-color: #E07A5F;
                    color: #3D3D3D;  
                    border: 3px solid black;
                    border-radius: 15px;
                }
""")    
        footer_layout_container = QWidget()

        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0,0,0,0)
        footer_layout.addWidget(self.label_7)
        footer_layout_container.setLayout(footer_layout)
        footer_layout_container.setFixedHeight(60)  # or whatever height fits your design
        # footer_layout_container.setStyleSheet("border: 2px dashed red; background-color: rgba(255, 0, 0, 30);")


        main_layout.addWidget(title_layout_container)
        main_layout.addWidget(recipe_name_layout_container)
        main_layout.addLayout(label_layout)
        main_layout.addLayout(ing_inst_layout)
        main_layout.addWidget(footer_layout_container)  

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
              print("Connecting to DB at:", db_path)

              conn = sqlite3.connect(get_writable_db_path())
              c = conn.cursor()
              c.execute(
                'INSERT INTO Recipes (RecipeName, Ingredients, Instructions, visible) VALUES (?, ?, ?, ?)',
                (self.RecipeName, self.ingredient, self.instructions, 1)
            )
              conn.commit()
              conn.close()
              self.label_7.show()
              self.label_7.setText('Recipe Added!')
              QTimer.singleShot(5000, self.label_7.hide)

    def new_recipe(self):
            self.Recipe_Name.clear()   
            self.Ingredients.clear()   
            self.Instructions.clear()

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

    def launch_list_window(self):
            try:
                self.recipe_list_window = RecipeListWindow(self)
                self.recipe_list_window.show()
            except Exception as e:
                import traceback
                traceback.print_exc()

    converter_window = None

    def open_converter(self):
        # Create and show the second page
        self.sec_win = SecondWindow()
        self.sec_win.show()
    

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