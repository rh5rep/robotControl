from PyQt5.QtCore import QThread, Signal
import numpy as np
from picamera import PiCamera


class CameraThread(QThread):
    new_frame = Signal(np.ndarray)

    def __init__(self, camera_id):
        super().__init__()
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)  # Set the desired resolution

    def run(self):
        self.camera.start_preview()
        while True:
            frame = np.empty((480, 640, 3), dtype=np.uint8)
            self.camera.capture(frame, 'bgr', use_video_port=True)
            self.new_frame.emit(frame)

    def stop_camera(self):
        self.camera.stop_preview()