import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QRadioButton, QLabel, QSpinBox, QTextEdit, QSlider, QLineEdit
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__nit__()
        self.setWindowTitle("G-code Move Commands")
        self.setGeometry(100, 100, 300, 300)

        # Create the main layout
        layout = QVBoxLayout()

        # Create radio buttons for selecting movement type
        self.incremental_radio = QRadioButton("Incremental Movement")
        self.incremental_radio.setChecked(True)
        self.incremental_radio.toggled.connect(self.set_movement_type)
        layout.addWidget(self.incremental_radio)

        self.absolute_radio = QRadioButton("Absolute Movement")
        self.absolute_radio.toggled.connect(self.set_movement_type)
        layout.addWidget(self.absolute_radio)

        # Create a spin box for choosing the amount to move
        self.move_amount_spinbox = QSpinBox()
        self.move_amount_spinbox.setMinimum(1)
        self.move_amount_spinbox.setMaximum(100)
        layout.addWidget(self.move_amount_spinbox)

        # Create a slider for choosing the movement speed
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(10)
        layout.addWidget(QLabel("Speed:"))
        layout.addWidget(self.speed_slider)

        # Create push buttons for each G-code move command
        move_up_button = QPushButton("Move Up")
        move_up_button.clicked.connect(self.send_gcode_up)
        layout.addWidget(move_up_button)

        move_down_button = QPushButton("Move Down")
        move_down_button.clicked.connect(self.send_gcode_down)
        layout.addWidget(move_down_button)

        move_left_button = QPushButton("Move Left")
        move_left_button.clicked.connect(self.send_gcode_left)
        layout.addWidget(move_left_button)

        move_right_button = QPushButton("Move Right")
        move_right_button.clicked.connect(self.send_gcode_right)
        layout.addWidget(move_right_button)

        # Create a stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_gcode)
        layout.addWidget(self.stop_button)

        # Create an input text field for manual G-code entry
        self.gcode_input = QLineEdit()
        layout.addWidget(self.gcode_input)

        # Create a text box to display the sent/received G-code commands
        self.gcode_display = QTextEdit()
        self.gcode_display.setReadOnly(True)
        layout.addWidget(self.gcode_display)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Serial connection settings
        self.serial_port = "/dev/ttygUSB0"  # Replace with the appropriate port
        self.baud_rate = 115200  # Replace with the appropriate baud rate

        # Open the serial connection
        self.serial = serial.Serial(self.serial_port, self.baud_rate)

        # Movement type (incremental or absolute)
        self.movement_type = "G91"  # G91: Incremental movement

    def read_serial_response(self):
        while self.serial.in_waitiing:
            response = self.serial.readline().decode.strip()
            # Process the response as needed
            print(f"Received response: {response}")

    def set_movement_type(self):
        if self.incremental_radio.isChecked():
            self.movement_type = "G91"  # G91: Incremental movement
        elif self.absolute_radio.isChecked():
            self.movement_type = "G90"  # G90: Absolute movement

    def send_gcode(self, gcode_command):
        # Print the G-code command
        print("Sending G-code:", gcode_command)

        # Append the G-code command to the text box
        self.gcode_display.append(gcode_command)

        # Send the G-code command over the serial connection
        self.serial.write(gcode_command.encode())

        # Read and process the serial response
        self.read_serial_response()

    def send_gcode_up(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_slider.value()
        gcode_command = f"{self.movement_type} G1 Y{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_down(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_slider.value()
        gcode_command = f"{self.movement_type} G1 Y-{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_left(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_slider.value()
        gcode_command = f"{self.movement_type} G1 X-{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_right(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_slider.value()
        gcode_command = f"{self.movement_type} G1 X{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def stop_gcode(self):
        self.serial.write("M112\n".encode())  # Send the emergency stop command

    def send_custom_gcode(self):
        gcode_command = self.gcode_input.text() + "\n"
        self.send_gcode(gcode_command)
        self.gcode_input.clear()

    def resizeEvent(self, event):
        self.gcode_display.resize(event.size())


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
