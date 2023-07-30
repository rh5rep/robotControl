import ast
from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout, \
    QPushButton, QLineEdit, QTextEdit, QSpacerItem, QSizePolicy, QRadioButton, QSpinBox, QComboBox, QHBoxLayout, \
    QFormLayout, QDoubleSpinBox

from movement import Movement


class SchedulerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.gcode_commands = []
        self.index = None
        self.amount_add_pressed = 0
        self.task_data = []
        self.row_data = []

        self.movement = Movement()

        # Tab 2
        # vertical
        # - horizontal- add label, drop, drop, drop
        # - button
        # - horizontal - add label, radio cam 1, cam 2, off

        # TODO make a dialog box to ask how many jibs and tools there are

        jib_range = [1, 4]
        jib_array = ['1', '2', '3', '4']
        tool_array = ['Power Sensor', 'Spectrum Analyzer', 'Cal Standard', 'Inspection', 'Plug and Wait', 'None']
        plug_array = []
        for num in range(1, 19):
            plug_array.append(str(num))

        jib_spinbox = QSpinBox()
        jib_spinbox.setRange(jib_range[0], jib_range[1])
        plug_spinbox = QSpinBox()
        plug_spinbox.setRange(1, 18)

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


        # Tab 3
        tab3_V_layout = QVBoxLayout()
        choose_form = QFormLayout()

        choose_form.addRow('Tool:', tool_combo)

        choose_form.addRow('Jib #: ', jib_spinbox)
        choose_form.addRow('Position #: ', plug_spinbox)

        self.task_form = QFormLayout()
        form_H_box = QHBoxLayout()

        self.insert_spinbox = QSpinBox()
        self.insert_spinbox.setRange(1, self.task_form.rowCount())
        choose_form.addRow('Insert as Task #: ', self.insert_spinbox)

        self.wait_spinbox = QSpinBox()
        self.wait_spinbox.setRange(0, 60)
        choose_form.addRow('Wait Time: ', self.wait_spinbox)

        self.distance_spinbox = QDoubleSpinBox()
        self.distance_spinbox.setRange(1, 20)
        choose_form.addRow('Z Travel: ', self.distance_spinbox)

        self.feedrate_spinbox = QDoubleSpinBox()
        self.feedrate_spinbox.setRange(50, 300)
        choose_form.addRow('Feedrate: ', self.feedrate_spinbox)

        add_button = QPushButton('Add')
        save_button = QPushButton('Save')
        load_button = QPushButton('Load')
        run_button = QPushButton('Run')

        add_button.clicked.connect(
            lambda: self.add_row(tool_combo.currentText(), jib_spinbox.value(), plug_spinbox.value()))
        save_button.clicked.connect(lambda: self.save_tasks())
        load_button.clicked.connect(lambda: self.load_tasks())
        run_button.clicked.connect(lambda: self.run())

        form_H_box.addWidget(save_button)
        form_H_box.addWidget(load_button)

        tab3_V_layout.addLayout(self.task_form)
        tab3_V_layout.addLayout(form_H_box)
        tab3_V_layout.addLayout(choose_form)
        tab3_V_layout.addWidget(add_button)
        tab3_V_layout.addWidget(run_button)

        self.setLayout(tab3_V_layout)

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

    def run(self):
        self.update_form()
        # X Y Z E
        # Assuming Plug 1 is Home then absolute from there
        jib1_plug_dict = {
            1: [0, 0, 0, 0],
            2: [0, 15, 0, 15],
            3: [9.5, 17.35, 0, 17.35],
            4: [9.5, 2.5, 0, 2.5]
        }
        jib2_plug_dict = {
            1: [0, 0, 0, 0]
        }
        self.gcode_commands = []
        for sublist in self.task_data:
            # print(f'sublist: {sublist}')
            tool = sublist[0]
            jib = sublist[1]
            plug = sublist[2]

            if jib == 1:
                if plug <= len(jib1_plug_dict):
                    self.gcode_commands.append(
                        f'G90\nG1 X{str(jib1_plug_dict[plug][0])} Y{str(jib1_plug_dict[plug][1])} Z{str(jib1_plug_dict[plug][2])} E{str(jib1_plug_dict[plug][3])} F{self.feedrate_spinbox.value()}\n' )
                    # ~ self.gcode_commands.append(
                        # ~ f'G1 Z{self.distance_spinbox.value()}\n')
                    # ~ self.gcode_commands.append(
                        # ~ f'G4 P{self.wait_spinbox.value()*1000}\n')
                    # ~ self.gcode_commands.append(
                        # ~ f'G1 Z-{self.distance_spinbox.value()}\n')
                    # ~ self.gcode_commands.append(
                        # ~ f'G4 P{self.wait_spinbox.value()*1000}\n')
                else:
                    print(f"plug {plug} not available")

                # print(f"g{self.gcode_commands}")
        self.movement.from_scheduler(self.gcode_commands)
