import sys
import os
import sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtPrintSupport import *
from recipe_list_window import RecipeListWindow
from converter import SecondWindow
# from recipe_keeper import RecipeKeeper

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)
db_path = resource_path("Recipe_keeper.db")
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database not found at {db_path}")

