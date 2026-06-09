import sys
import os
from PySide6.QtWidgets import QApplication
from ui.login import MainWindow
from ui.register import RegisterPage

def load_stylesheet(app, file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load QSS
    style_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    load_stylesheet(app, style_path)
    
    window = RegisterPage()
    window.show()
    
    sys.exit(app.exec())