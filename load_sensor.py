import platform

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO  # import GPIO
    from hx711 import HX711  # import the class HX711
from PyQt5.QtCore import QThread, pyqtSignal as Signal
import time, random

class LoadSensorThread(QThread):
    new_data = Signal(list)

    def run(self):
        start_time = time.time()
        ratio = -212.99
        readings = 5

        if platform.system() != 'Windows':
            GPIO.setmode(GPIO.BCM)
            hx = HX711(dout_pin=21, pd_sck_pin= 20)
            load_sensor_data = hx.zero(readings)
            hx.set_scale_ratio(ratio)

        while True:
            current_time = time.time() - start_time
            if platform.system() == 'Windows':
                load_sensor_data = random.randint(1,100)
            else:
                load_sensor_data = hx.get_weight_mean(readings)

            load_and_time = [current_time, load_sensor_data]
            self.new_data.emit(load_and_time)
            time.sleep(0.1)
