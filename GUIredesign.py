import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout, \
    QPushButton, QLineEdit, QTextEdit, QSpacerItem, QSizePolicy, QHBoxLayout, QComboBox, QRadioButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Control")
        self.setGeometry(100, 100, 500, 400)

        # Create a central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create the tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Create the tabs
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Add tabs to the tab widget
        tab_widget.addTab(tab1, "Manual Control")
        tab_widget.addTab(tab2, "Semi-Auto Control")
        tab_widget.addTab(tab3, "Tool Change")

        # Customize the tab content
        tab1_layout = QVBoxLayout(tab1)
        tab1_grid_layout = QGridLayout(tab1)
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

        # Create an input text field for manual G-code entry
        self.gcode_input = QLineEdit()
        self.gcode_input.setPlaceholderText("Send Manual G-Code")

        # Create a Read-Only text field for Echoing G-code
        self.gcode_display = QTextEdit()
        self.gcode_display.setReadOnly(True)
        self.gcode_display.setPlaceholderText("G-Code Echo from Creality Board")

        tab1_layout.addWidget(self.gcode_input)
        tab1_layout.addWidget(self.gcode_display)

        # Tab 2
        # vertical
        # - horizontal- add label, drop, drop, drop
        # - button
        # - horizontal - add label, radio cam 1, cam 2, off
        jib_array = ['Jib position', '1', '2', '3', '4']
        tool_array = ['Tool', 'Power', 'Cable', 'None']
        plug_array = ['Plug position']
        for num in range(1, 19):
            plug_array.append(str(num))

        tab2_V_layout = QVBoxLayout(tab2)
        tab2_H1_layout = QHBoxLayout(tab2)

        goto_label = QLabel("Go to: ")
        tool_combo = QComboBox()
        tool_combo.addItems(tool_array)
        tool_combo.setCurrentText(tool_array[0])
        jib_combo = QComboBox()
        jib_combo.addItems(jib_array)
        jib_combo.setCurrentText(jib_array[0])
        plug_combo = QComboBox()
        plug_combo.addItems(plug_array)
        plug_combo.setCurrentText(plug_array[0])

        tab2_H1_layout.addWidget(goto_label)
        tab2_H1_layout.addWidget(tool_combo)
        tab2_H1_layout.addWidget(jib_combo)
        tab2_H1_layout.addWidget(plug_combo)

        tab2_V_layout.addLayout(tab2_H1_layout)
        tab2_V_layout.addWidget(QPushButton("Go"))

        # Cam Stuff

        cam_array = ['None', 'Cam 1', 'Cam 2']
        tab2_H2_layout = QHBoxLayout(tab2)
        tab2_H2_layout.addWidget(QLabel("View: "))
        tab2_H2_layout.addStretch()

        tab2_H2_layout.addStretch()
        cam_combo = QComboBox()
        cam_combo.addItems(cam_array)
        cam_combo.setCurrentText('None')

        view_button = QPushButton('View')

        tab2_H2_layout.addWidget(cam_combo)
        tab2_H2_layout.addWidget(view_button)
        tab2_V_layout.addLayout(tab2_H2_layout)

        # Tool Stuff

        tab2_H3_layout = QHBoxLayout()
        tab2_H3_layout.addWidget(tool_combo)
        tab2_H3_layout.addWidget(QPushButton("Change"))

        tab2_V_layout.addLayout(tab2_H3_layout)

        # Tab 3
        tab3_layout = QVBoxLayout(tab3)
        tab2_H2_layout = QHBoxLayout(tab2)
        tab2_H2_layout.addWidget(QLabel("View"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
