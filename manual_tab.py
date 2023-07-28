from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout, \
    QPushButton, QLineEdit, QTextEdit, QSpacerItem, QSizePolicy, QRadioButton, QSpinBox, QComboBox, QHBoxLayout, \
    QFormLayout

from movement import Movement


class ManualTab(QWidget):

    def __init__(self):
        super().__init__()

        self.movement = Movement()

        # Customize the tab content
        tab1_layout = QVBoxLayout()
        tab1_grid_layout = QGridLayout()
        tab1_layout.addLayout(tab1_grid_layout)

        # Create the buttons for the grid
        button_y_plus = QPushButton("Y+")
        button_x_minus = QPushButton("X-")
        button_home = QPushButton("Home")
        button_x_plus = QPushButton("X+")
        button_y_minus = QPushButton("Y-")
        button_z_plus = QPushButton("Z+")
        button_z_minus = QPushButton("Z-")

        # Set the size policy for the buttons
        button_y_plus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_x_minus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_home.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_x_plus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_y_minus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_z_plus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_z_minus.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the buttons to the grid
        tab1_grid_layout.addWidget(button_y_plus, 0, 1)
        tab1_grid_layout.addWidget(button_x_minus, 1, 0)
        tab1_grid_layout.addWidget(button_home, 1, 1)
        tab1_grid_layout.addWidget(button_x_plus, 1, 2)
        tab1_grid_layout.addWidget(button_y_minus, 2, 1)
        tab1_grid_layout.addWidget(button_z_plus, 0, 4)
        tab1_grid_layout.addWidget(button_z_minus, 2, 4)

        # Create horizontal and vertical spacers
        hspacer = QSpacerItem(30, 10, QSizePolicy.Expanding, QSizePolicy.Fixed)
        vspacer = QSpacerItem(10, 30, QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Add the spacers to the grid layout
        tab1_grid_layout.addItem(hspacer, 0, 0)
        tab1_grid_layout.addItem(hspacer, 0, 4)
        tab1_grid_layout.addItem(vspacer, 4, 0, 1, 5)

        # Create radio buttons for selecting movement type
        self.incremental_radio = QRadioButton("Incremental Movement")
        self.incremental_radio.setChecked(True)
        self.incremental_radio.toggled.connect(partial(self.movement.set_movement_type, True))
        tab1_layout.addWidget(self.incremental_radio)
        self.absolute_radio = QRadioButton("Absolute Movement")
        self.absolute_radio.toggled.connect(partial(self.movement.set_movement_type, False))
        tab1_layout.addWidget(self.absolute_radio)
        # Create a spin box for choosing the amount to move
        self.move_amount_spinbox = QSpinBox()
        self.move_amount_spinbox.setMinimum(1)
        self.move_amount_spinbox.setMaximum(10000)
        tab1_layout.addWidget(self.move_amount_spinbox)

        # Create a slider for choosing the movement speed
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setMinimum(1)
        self.speed_spinbox.setMaximum(500)
        self.speed_spinbox.setValue(50)
        tab1_layout.addWidget(QLabel("Speed:"))
        tab1_layout.addWidget(self.speed_spinbox)

        # Create an input text field for manual G-code entry
        self.gcode_input = QLineEdit()
        self.gcode_input.setPlaceholderText("Send Manual G-Code")
        self.gcode_input.returnPressed.connect(partial(self.movement.send_custom_gcode, self.gcode_input.text()))

        # Create a Read-Only text field for Echoing G-code
        self.gcode_display = QTextEdit()
        self.gcode_display.setReadOnly(True)
        self.gcode_display.setPlaceholderText("G-Code Echo from Creality Board")
        self.movement.gcode_display_updated.connect(self.update_gcode_display)

        tab1_layout.addWidget(self.gcode_input)
        tab1_layout.addWidget(self.gcode_display)

        self.setLayout(tab1_layout)

        # Movement

        # button_y_plus.clicked.connect(
        #     partial(self.movement.send_gcode_forward, self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        # button_y_minus.clicked.connect(
        #     partial(self.movement.send_gcode_back, self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        # button_x_plus.clicked.connect(
        #     partial(self.movement.send_gcode_right, self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        # button_x_minus.clicked.connect(
        #     partial(self.movement.send_gcode_left, self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        # button_z_plus.clicked.connect(
        #     partial(self.movement.send_gcode_up, self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        # button_z_minus.clicked.connect(
        #     partial(self.movement.send_gcode_down, self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        # button_home = QPushButton("Home")

        button_y_plus.clicked.connect(
            lambda: self.movement.send_gcode_forward(self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        button_y_minus.clicked.connect(
            lambda: self.movement.send_gcode_back(self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        button_x_plus.clicked.connect(
            lambda: self.movement.send_gcode_right(self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        button_x_minus.clicked.connect(
            lambda: self.movement.send_gcode_left(self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        button_z_plus.clicked.connect(
            lambda: self.movement.send_gcode_up(self.move_amount_spinbox.value(), self.speed_spinbox.value()))
        button_z_minus.clicked.connect(
            lambda: self.movement.send_gcode_down(self.move_amount_spinbox.value(), self.speed_spinbox.value()))
    def update_gcode_display(self, gcode_command):
        self.gcode_display.append(gcode_command)