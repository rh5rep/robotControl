from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
from load_sensor import LoadSensorThread
import pyqtgraph as pg

class DataAndCamsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.load_sensor_label = QLabel(f"Load Sensor Data: N/A")
        self.read_button = QCheckBox()
        self.read_button.setText('Plot Data?: ')
        layout = QVBoxLayout()
        layout.addWidget(self.load_sensor_label)
        layout.addWidget(self.read_button)

        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)
        self.setLayout(layout)

        # Create LoadSensorThread:
        self.load_sensor_thread = LoadSensorThread()
        self.load_sensor_thread.new_data.connect(self.update_load_sensor_label)
        self.load_sensor_thread.start()

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
