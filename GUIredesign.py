import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout, \
    QPushButton, QLineEdit, QTextEdit, QSpacerItem, QSizePolicy, QRadioButton, QSpinBox

from movement import Movement
from data_and_cams import DataAndCamsTab
from scheduler import SchedulerTab
from manual_tab import ManualTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.index = None
        self.amount_add_pressed = 0
        self.task_data = []
        self.row_data = []
        self.setWindowTitle("Robot Control")
        self.setGeometry(100, 100, 500, 400)

        self.load_sensor_data_label = QLabel()

        self.movement = Movement()

        # Create a central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create the tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Create the tabs
        tab1 = ManualTab()
        tab2 = SchedulerTab()
        tab4 = DataAndCamsTab()
        # Add tabs to the tab widget
        tab_widget.addTab(tab1, "Manual Control")
        tab_widget.addTab(tab2, "Tool Change")
        tab_widget.addTab(tab4, "Data and Cams")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
