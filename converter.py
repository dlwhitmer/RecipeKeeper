import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import  *
from PyQt6.QtCore import *
import math
# from test2 import EmailWindow

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
  
        self.setWindowTitle("Measurement & °C/F Converter")
        self.setGeometry(500, 200, 600, 450)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("""
                QWidget{
        background-color: #FDF6E3; 
}
""")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._is_dragging = False
        self._drag_start_position = QPoint()
        
       
        self.title = QLabel(self)
        self.title.setText("Measurement & °C/F Converter")
        mfont = QFont("Times New Roman", 25)
        mfont.setBold(True)
        self.title.setFont(mfont)
        self.title.setFixedSize(500, 50)
        self.title.move(50,5)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel{
            background-color: #E07A5F;
            border: 2px solid #3D3D3D;
            border-radius: 15px;   
            color:#3D3D3D; 
            }
""")
        
        self.ounce_label_1 = QLabel("Ounces",self)
        ofont = QFont("Times New Roman", 15)
        ofont.setBold(True)
        self.ounce_label_1.setFont(ofont)
        self.ounce_label_1.setFixedSize(75,40)
        self.ounce_label_1.move(66,68)
        self.ounce_label_1.setStyleSheet("color:#3D3D3D;")

        self.ounces_1 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.ounces_1.setFont(mfont)
        self.ounces_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ounces_1.move(25, 100)
        self.ounces_1.setFixedSize(150, 50)
        self.ounces_1.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        self.to_label_1 = QLabel(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.to_label_1.setFont(mfont)
        self.to_label_1.setText("To")
        self.to_label_1.setFixedSize(40, 40)
        self.to_label_1.move(184,100)
        self.to_label_1.setStyleSheet("color:#3D3D3D;")
        
        self.grams_label = QLabel("Grams",self)
        ofont = QFont("Times New Roman", 15)
        ofont.setBold(True)
        self.grams_label.setFont(ofont)
        self.grams_label.setFixedSize(75,40)
        self.grams_label.move(265,68)
        self.grams_label.setStyleSheet("color:#3D3D3D;")


        self.grams_1 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.grams_1.setFont(mfont)
        self.grams_1.move(225, 100)
        self.grams_1.setFixedSize(150, 50)
        self.grams_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grams_1.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        self.btn_1 = QPushButton("Convert To\nGrams", self)
        self.btn_1.clicked.connect(self.ounces_to_grams)
        mfont = QFont("Times New Roman", 15)
        mfont.setBold(True)
        self.btn_1.setFont(mfont)
        self.btn_1.move(400, 100)
        self.btn_1.setFixedSize(150, 50)
        self.btn_1.setStyleSheet("""
        QPushButton{
        background-color: #81B29A;
        color: #3D3D3D;
        }
""")
    
        self.grams_2 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.grams_2.setFont(mfont)
        self.grams_2.move(25, 175)
        self.grams_2.setFixedSize(150, 50)
        self.grams_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grams_2.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        self.grams_label_2 = QLabel("Grams",self)
        ofont = QFont("Times New Roman", 15)
        ofont.setBold(True)
        self.grams_label_2.setFont(ofont)
        self.grams_label_2.setFixedSize(75,25)
        self.grams_label_2.move(66,150)
        self.grams_label_2.setStyleSheet("color:#3D3D3D;")

        self.to_label_2 = QLabel(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.to_label_2.setFont(mfont)
        self.to_label_2.setText("To")
        self.to_label_2.setFixedSize(40, 50)
        self.to_label_2.move(184,170)
        self.to_label_2.setStyleSheet("color:#3D3D3D;")
        
        self.grams_label_2 = QLabel("Ounces",self)
        ofont = QFont("Times New Roman", 15)
        ofont.setBold(True)
        self.grams_label_2.setFont(ofont)
        self.grams_label_2.setFixedSize(75,25)
        self.grams_label_2.move(265,150)
        self.grams_label_2.setStyleSheet("color:#3D3D3D;")
     
        self.ounces_2 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.ounces_2.setFont(mfont)
        self.ounces_2.move(225, 175)
        self.ounces_2.setFixedSize(150, 50)
        self.ounces_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ounces_2.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        self.btn_2 = QPushButton("Convert To\nOunces", self)
        self.btn_2.clicked.connect(self.grams_to_ounces)
        mfont = QFont("Times New Roman", 15)
        mfont.setBold(True)
        self.btn_2.setFont(mfont)
        self.btn_2.move(400, 170)
        self.btn_2.setFixedSize(150, 50)
        self.btn_2.setStyleSheet("""
        QPushButton{
        background-color: #81B29A;
        color: #3D3D3D;
        }
""")
        
        
        self.Celsius_1 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.Celsius_1.setFont(mfont)
        self.Celsius_1.move(25, 250)
        self.Celsius_1.setFixedSize(150, 50)
        self.Celsius_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Celsius_1.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        self.to_label_3 = QLabel(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.to_label_3.setFont(mfont)
        self.to_label_3.setText("To")
        self.to_label_3.setFixedSize(40, 50)
        self.to_label_3.move(184,250)
        self.to_label_3.setStyleSheet("color:#3D3D3D;")
        
        self.Fahrenheit_1 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.Fahrenheit_1.setFont(mfont)
        self.Fahrenheit_1.move(225, 250)
        self.Fahrenheit_1.setFixedSize(150, 50)
        self.Fahrenheit_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Fahrenheit_1.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        self.far_label_1 = QLabel("Fahrenheit",self)
        self.far_label_1.setFont(ofont)
        self.far_label_1.setFixedSize(100,25)
        self.far_label_1.move(250,225)
        self.far_label_1.setStyleSheet("color:#3D3D3D;")
        
        self.cel_label_1 = QLabel("Celsius",self)
        self.cel_label_1.setFont(ofont)
        self.cel_label_1.setFixedSize(100,25)
        self.cel_label_1.move(70,225)
        self.cel_label_1.setStyleSheet("color:#3D3D3D;")

        self.btn_3 = QPushButton("Convert To\nFahrenheit", self)
        self.btn_3.clicked.connect(self.celcius_to_farh)
        mfont = QFont("Times New Roman", 15)
        mfont.setBold(True)
        self.btn_3.setFont(mfont)
        self.btn_3.move(400, 240)
        self.btn_3.setFixedSize(150, 50)
        self.btn_3.setStyleSheet("""
        QPushButton{
        background-color: #81B29A;
        color:#3D3D3D;
        }
""")

        self.Celsius_2 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.Celsius_2.setFont(mfont)
        self.Celsius_2.move(225, 325)
        self.Celsius_2.setFixedSize(150, 50)
        self.Celsius_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Celsius_2.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        self.to_label_4 = QLabel(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.to_label_4.setFont(mfont)
        self.to_label_4.setText("To")
        self.to_label_4.setFixedSize(40, 50)
        self.to_label_4.move(184,325)
        self.to_label_4.setStyleSheet("color:#3D3D3D;")
        
        self.Fahrenheit_2 = QLineEdit(self)
        mfont = QFont("Times New Roman", 18)
        mfont.setBold(True)
        self.Fahrenheit_2.setFont(mfont)
        self.Fahrenheit_2.move(25, 325)
        self.Fahrenheit_2.setFixedSize(150, 50)
        self.Fahrenheit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Fahrenheit_2.setStyleSheet("""
        QLineEdit{
            background-color: #fff0d4;
            border: 2px solid #3D3D3D;
            border-radius: 15px;
            color:#3D3D3D;
        }
""")
        
        self.far_label_2 = QLabel("Fahrenheit",self)
        self.far_label_2.setFont(ofont)
        self.far_label_2.setFixedSize(100,25)
        self.far_label_2.move(50,300)
        self.far_label_2.setStyleSheet("color:#3D3D3D;")
        
        self.cel_label_2 = QLabel("Celsius",self)
        self.cel_label_2.setFont(ofont)
        self.cel_label_2.setFixedSize(100,25)
        self.cel_label_2.move(266,300)
        self.cel_label_2.setStyleSheet("color:#3D3D3D;")

        self.btn_4 = QPushButton("Convert To\nFahrenheit", self)
        self.btn_4.clicked.connect(self.Farh_to_cel)
        mfont = QFont("Times New Roman", 15)
        mfont.setBold(True)
        self.btn_4.setFont(mfont)
        self.btn_4.move(400, 325)
        self.btn_4.setFixedSize(150, 50)
        self.btn_4.setStyleSheet("""
        QPushButton{
        background-color: #81B29A;
        color: #3D3D3D;
        }
""")
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.clear_btn = QPushButton("Clear All Fields",self)
        button_layout.addWidget(self.clear_btn)
        cfont = QFont("Times New Roman", 15)
        cfont.setBold(True)
        self.clear_btn.setFont(cfont)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.clear_btn.setFixedSize(150,40)
        self.clear_btn.move(120,385)
        self.clear_btn.setStyleSheet("""
        QPushButton{
        background-color: #81B29A;
        border: 2px solid #3D3D3D;
        border-radius: 15px;
        color: #3D3D3D;
        }
        
""")
        
        
        self.exit_btn = QPushButton("Exit",self)
        self.exit_btn.clicked.connect(self.close)
        button_layout.addWidget(self.exit_btn)
        cfont = QFont("Times New Roman", 15)
        cfont.setBold(True)
        self.exit_btn.setFont(cfont)
     
        self.exit_btn.clicked.connect(self.clear_fields)
        self.exit_btn.setFixedSize(150,40)
        self.exit_btn.move(290,385)
        self.exit_btn.setStyleSheet("""
        QPushButton{
        background-color: #81B29A;
        border: 2px solid #3D3D3D;
        border-radius: 15px;
        color: #3D3D3D;
        }
        
""")

    def clear_fields(self):    
        self.ounces_1.clear()
        self.ounces_2.clear()
        self.grams_1.clear()
        self.grams_2.clear()
        self.Fahrenheit_1.clear()
        self.Fahrenheit_2.clear()
        self.Celsius_1.clear()
        self.Celsius_2.clear()
        


    def truncate_to_two_places(number):
        return math.trunc(number * 100) / 100    


    def ounces_to_grams(self):
        # Get the text from the input field
        ounces = self.ounces_1.text()
        try:
            # Convert the input to a number (float or int)
            number1 = float(ounces) if '.' in ounces else int(ounces)
            grams = (number1 * 28.34952)
            res = round(grams, 2)
            self.grams_1.setText(str(res))

        except ValueError:
            print("Invalid input! Please enter a valid number.")


    def grams_to_ounces(self):
        # Get the text from the input field
        grams = self.grams_2.text()
        try:
            # Convert the input to a number (float or int)
            number2 = float(grams) if '.' in grams else int(grams)
            ounces = (number2 * 0.035274)
            res1 = round(ounces, 2)
            self.ounces_2.setText(str(res1))

        except ValueError:
            print("Invalid input! Please enter a valid number.")        
    
    def celcius_to_farh(self):
        # Get the text from the input field
        celcius = self.Celsius_1.text()
        try:
            # Convert the input to a number (float or int)
            number3 = float(celcius) if '.' in celcius else int(celcius)
            farh = (number3 * 1.8)+32
            print(farh)
            res2 = round(farh, 2)
            self.Fahrenheit_1.setText(str(res2))

        except ValueError:
            print("Invalid input! Please enter a valid number.") 
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


    def Farh_to_cel(self):
        # Get the text from the input field
        farh2 = self.Fahrenheit_2.text()
        try:
            # Convert the input to a number (float or int)
            number3 = float(farh2) if '.' in farh2 else int(farh2)
            Celcius = (number3 - 32)/1.8
            res3 = round(Celcius, 2)
            self.Celsius_2.setText(str(res3))

        except ValueError:
            print("Invalid input! Please enter a valid number.")        

# app = QApplication([])
# window = SecondWindow()
# window.show()
# app.exec()
