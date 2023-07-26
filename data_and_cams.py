import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
from load_sensor import LoadSensorThread
from camera import CameraThread
import pyqtgraph as pg

class DataAndCamsTab(QWidget):
    def __init__(self):
        super().__init__()

        camera_id = 0

        self.load_sensor_label = QLabel(f"Load Sensor Data: N/A")
        self.read_button = QCheckBox()
        self.read_button.setText('Plot Data?: ')
        self.camera_button = QCheckBox()
        self.camera_button.setText('Show Camera?: ')

        self.camera_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.load_sensor_label)
        layout.addWidget(self.read_button)
        layout.addWidget(self.camera_button)

        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)
        self.setLayout(layout)


        # Create LoadSensorThread:
        self.load_sensor_thread = LoadSensorThread()
        self.load_sensor_thread.new_data.connect(self.update_load_sensor_label)
        self.load_sensor_thread.start()

        # Create CameraThread:
        self.camera_thread = CameraThread(camera_id)
        self.camera_thread.new_frame.connect(self.update_camera(self.update_camera))

        # Initialize data lists:

        self.timestamp = []
        self.load_data = []


    def update_load_sensor_label(self, data):

        timestamp, load_sensor_data = data[0], data[1]

        # if timestamp >= 10:
        if self.read_button.isChecked():

            self.load_sensor_label.setText(f"Load Sensor Data: {load_sensor_data}")

            self.timestamp.append(timestamp)
            self.load_data.append(load_sensor_data)

            self.graphWidget.plot(self.timestamp, self.load_data)

        else:
            self.graphWidget.clear()
            self.timestamp = []
            self.load_data = []

    def update_camera(self, frame):
        if self.camera_button.isChecked():
            height, width, bytes = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.camera_label.setPixmap(pixmap)

        else:
            self.camera_thread.stop_camera()
            self.camera_label.clear()




