import platform
import time
import random

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO
    from hx711 import HX711

from PyQt5.QtCore import QThread, pyqtSignal as Signal


class LoadSensorThread(QThread):
    new_data = Signal(list)

    def run(self):
        start_time = time.time()
        ratio = -212.99
        NumReadings = 10

        if platform.system() != 'Windows':
            GPIO.setmode(GPIO.BCM)
            hx = HX711(dout_pin=21, pd_sck_pin=20, gain=128, channel='A')

            # Calibrate the HX711 and set the scale ratio and tare weight
            print("Reset")
            result = hx.reset()		# Before we start, reset the hx711 ( not necessary)
            if result:			# you can check if the reset was successful
                print('Ready to use')
            else:
                print('not ready')

            # hx.set_scale_ratio(ratio)

        while True:
            current_time = time.time() - start_time
            if platform.system() == 'Windows':
                load_sensor_data = random.randint(1, 100)
            else:
                # Use hx.get_weight_mean() with a delay between readings
                # ~ load_sensor_data = self.get_weight_with_delay(hx, NumReadings, 0.1)
                load_sensor_data = hx.get_raw_data(NumReadings)
                load_sensor_data = sum(load_sensor_data)/len(load_sensor_data)

            load_and_time = [current_time, load_sensor_data]
            self.new_data.emit(load_and_time)

    # ~ def get_weight_with_delay(self, hx, num_readings, delay_between_readings):
        # ~ total_weight = 0
        # ~ for _ in range(num_readings):
            # ~ total_weight += hx.get_raw_data(num_readings)
            # ~ time.sleep(delay_between_readings)
        # ~ return total_weight / num_readings
