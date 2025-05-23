import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QRadioButton, QLabel, \
    QSpinBox, QTextEdit, QSlider, QLineEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from picamera import PiCamera

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.move_amount_spinbox.setMaximum(10000)
        layout.addWidget(self.move_amount_spinbox)
        # Create a slider for choosing the movement speed
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setMinimum(1)
        self.speed_spinbox.setMaximum(500)
        self.speed_spinbox.setValue(50)
        layout.addWidget(QLabel("Speed:"))
        layout.addWidget(self.speed_spinbox)
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
        self.gcode_input.returnPressed.connect(self.send_custom_gcode)
        layout.addWidget(self.gcode_input)
        # Create a text box to display the sent/received G-code commands
        self.gcode_display = QTextEdit()
        self.gcode_display.setReadOnly(True)
        layout.addWidget(self.gcode_display)
        # Create image label
        self.image_label = QLabel()
        layout.addWidget(self.image_label)
        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        # Serial connection settings
        self.serial_port = "/dev/ttyUSB0"  # Replace with the appropriate port
        self.baud_rate = 115200  # Replace with the appropriate baud rate

        # Open the serial connection
        self.serial = serial.Serial(self.serial_port, self.baud_rate)
        # Movement type (incremental or absolute)
        self.movement_type = "G91"  # G91: Incremental movement

        # Camera Stuff

        self.camera = PiCamera()
        self.camera.resolution = (640, 480)  # Set the desired resolution

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(100)


    def read_serial_response(self):
        while self.serial.in_waiting:
            response = self.serial.readline().decode("utf-8").strip()
            # Process the response as needed
            print(f"Received response: {response}")
            self.gcode_display.append(response)

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

        if self.serial:
            # Read and process the serial response
            self.read_serial_response()

    def send_gcode_up(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_spinbox.value()
        gcode_command = f"{self.movement_type} \nG1 Y{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_down(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_spinbox.value()
        gcode_command = f"{self.movement_type} \nG1 Y-{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_left(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_spinbox.value()
        gcode_command = f"{self.movement_type} \nG1 X-{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def send_gcode_right(self):
        move_amount = self.move_amount_spinbox.value()
        speed = self.speed_spinbox.value()
        gcode_command = f"{self.movement_type} \nG1 X{move_amount} F{speed}\n"
        self.send_gcode(gcode_command)

    def stop_gcode(self):
        self.serial.write("M112\n".encode())  # Send the emergency stop command

    def send_custom_gcode(self):
        gcode_command = self.gcode_input.text() + "\n"
        self.send_gcode(gcode_command)
        self.gcode_input.clear()

    def resizeEvent(self, event):
        self.gcode_display.resize(event.size())

    def update_camera_feed(self):

        # Capture camera image
        self.camera.capture("temp.jpg")

        # Load captured imaged
        image = QImage("temp.jpg")

        # Convert the image to QPixmap to display in a QLabel or other widget
        pixmap = QPixmap.fromImage(image)

        # Update the QLabel or other widget with the new pixmap
        # For example, if you have a QLabel called "image_label":
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        # Release camera and stop the timer
        self.camera.close()
        self.timer.stop()
        super().closeEvent(event)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
