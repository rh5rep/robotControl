# main.py
import sys
from PySide6.QtWidgets import QApplication
from GUIredesign import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
