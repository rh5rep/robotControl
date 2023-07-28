from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QTextEdit
import serial


class Movement(QObject):
    gcode_display_updated = pyqtSignal(str)  # Define a signal that carries a string
    def __init__(self):
        super().__init__()

        self.movement_type = "G91"
        self.speed = 1
        self.amount = 50

        # Create a Read-Only text field for Echoing G-code
        self.gcode_display = QTextEdit()
        self.gcode_display.setReadOnly(True)
        self.gcode_display.setPlaceholderText("G-Code Echo from Creality Board")

        # Serial

        self.serial_port = "/dev/ttyUSB0"
        self.baud_rate = 115200

        self.serial = serial.Serial(self.serial_port, self.baud_rate)


    def set_movement_type(self, incremental):
        if incremental:
            self.movement_type = "G91"  # G91: Incremental movement
        else:
            self.movement_type = "G90"  # G90: Absolute movement

    def send_gcode(self, gcode_command):
        # Print the G-code command
        print("Sending G-code:", gcode_command)
        # Append the G-code command to the text box
        self.gcode_display.append(gcode_command)
        # Send the G-code command over the serial connection
        self.serial.write(gcode_command.encode())

        if self.serial:
            # Read and process the serial response
            self.read_serial_response()
        self.gcode_display_updated.emit(gcode_command)

    def get_gcode_display(self):
        # print(f'self.gcode_display: {self.}')
        return self.gcode_display


    def send_gcode_up(self, move_amount, speed):
        gcode_command = f"{self.movement_type} \nG1 Z{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_down(self, move_amount, speed):
        gcode_command = f"{self.movement_type} \nG1 Z-{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_left(self, move_amount, speed):
        gcode_command = f"{self.movement_type} \nG1 X-{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_right(self, move_amount, speed):
        gcode_command = f"{self.movement_type} \nG1 X{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_forward(self, move_amount, speed):
        gcode_command = f"{self.movement_type} \nG1 Y{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_back(self, move_amount, speed):
        gcode_command = f"{self.movement_type} \nG1 Y-{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_custom_gcode(self):
        gcode_command = self.gcode_input.text() + "\n"
        self.send_gcode(gcode_command)
        self.gcode_input.clear()

    def read_serial_response(self):
        while self.serial.in_waiting:
            response = self.serial.readline().decode("utf-8").strip()
            # Process the response as needed
            print(f"Received response: {response}")
            self.gcode_display.append(response)

