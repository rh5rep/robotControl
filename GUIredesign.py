import ast
import sys
from functools import partial

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout, \
    QPushButton, QLineEdit, QTextEdit, QSpacerItem, QSizePolicy, QHBoxLayout, QComboBox, QRadioButton, QFormLayout, \
    QSpinBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.index = None
        self.amount_add_pressed = 0
        self.task_data = []
        self.row_data = []
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
        # tab_widget.addTab(tab2, "Semi-Auto Control")
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

        # TODO make a dialog box to ask how many jibs and tools there are

        jib_range = [1, 4]
        jib_array = ['1', '2', '3', '4']
        tool_array = ['Power', 'Cable', 'None']
        plug_array = []
        for num in range(1, 19):
            plug_array.append(str(num))

        jib_spinbox = QSpinBox()
        jib_spinbox.setRange(jib_range[0], jib_range[1])
        plug_spinbox = QSpinBox()
        plug_spinbox.setRange(1, 18)

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

        tab2_H2_layout = QHBoxLayout(tab2)
        tab2_H2_layout.addWidget(QLabel("View"))

        # Tab 3
        tab3_V_layout = QVBoxLayout(tab3)

        choose_form = QFormLayout()

        choose_form.addRow('Tool:', tool_combo)
        choose_form.addRow('Jib Number: ', jib_spinbox)
        choose_form.addRow('Plug Number: ', plug_spinbox)

        self.task_form = QFormLayout()
        form_H_box = QHBoxLayout()

        self.insert_spinbox = QSpinBox()
        self.insert_spinbox.setRange(1, self.task_form.rowCount())
        choose_form.addRow('Insert as Task #: ', self.insert_spinbox)

        add_button = QPushButton('Add')
        save_button = QPushButton('Save')
        load_button = QPushButton('Load')

        add_button.clicked.connect(
            lambda: self.add_row(tool_combo.currentText(), jib_spinbox.value(), plug_spinbox.value()))
        save_button.clicked.connect(lambda: self.save_tasks())
        load_button.clicked.connect(lambda: self.load_tasks())

        form_H_box.addWidget(save_button)
        form_H_box.addWidget(load_button)

        tab3_V_layout.addLayout(self.task_form)
        tab3_V_layout.addLayout(form_H_box)
        tab3_V_layout.addLayout(choose_form)
        tab3_V_layout.addWidget(add_button)
        tab3_V_layout.addWidget(QPushButton('Run'))

    def add_row(self, tool, jib, plug):

        self.amount_add_pressed += 1
        index = self.amount_add_pressed
        tool_button = QPushButton(f"Tool: {tool}")
        jib_button = QPushButton(f"Jib: {jib}")
        plug_button = QPushButton(f"Plug: {plug}")
        index_button = QPushButton(f"{index}")

        index_button.setVisible(False)

        row_addition = QHBoxLayout()
        row_addition.addWidget(tool_button)
        row_addition.addWidget(jib_button)
        row_addition.addWidget(plug_button)
        row_addition.addWidget(index_button)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(partial(self.remove_row, row_addition, index))

        row_addition.addWidget(remove_button)
        self.task_form.insertRow(self.insert_spinbox.value() - 1, f"Task #{self.insert_spinbox.value() + 1}",
                                 row_addition)
        self.insert_spinbox.setRange(0, self.task_form.rowCount() + 2)
        self.row_data = [tool, jib, plug, index]
        self.task_data.insert(self.insert_spinbox.value() - 1, self.row_data)
        self.update_form()

    def remove_row(self, row_layout, index):
        # Find the corresponding row layout in the form layout
        self.task_form.removeRow(row_layout)

        for i, sublist in enumerate(self.task_data):
            if sublist[3] == index:
                to_pop = i
                self.task_data.pop(to_pop)
        self.update_form()

    def update_form(self):
        for row in range(self.task_form.rowCount()):
            label_item = self.task_form.itemAt(row, QFormLayout.LabelRole)
            if label_item is not None and isinstance(label_item.widget(), QLabel):
                label_widget = label_item.widget()
                label_widget.setText(f"Task #{row + 1}:")
                self.insert_spinbox.setRange(1, self.task_form.rowCount() + 1)
                self.insert_spinbox.setValue(self.task_form.rowCount() + 1)

            if self.task_form.rowCount() < 1:
                self.insert_spinbox.setValue(1)

    def save_tasks(self):
        self.update_form()
        openfile = QtWidgets.QFileDialog.getOpenFileName(self)
        file = open(openfile[0], 'w')  # New line
        file.write(f"{self.task_data}")

    def load_tasks(self):
        openfile = QtWidgets.QFileDialog.getOpenFileName(self)
        file = open(openfile[0], 'r')  # New line
        data = file.read()  # New line
        data = ast.literal_eval(data)

        for sublist in data:
            tool = sublist[0]
            jib = sublist[1]
            plug = sublist[2]
            self.add_row(tool, jib, plug)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
