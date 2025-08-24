import time
import logging

from image_processing.camera.HomeSecurity import CameraDetector

camera_detector = CameraDetector()

time.sleep(5)

logging.warning("Starting camera 1")

camera_detector.start()

time.sleep(25)

logging.warning("Stopping camera 1")

camera_detector.stop()

time.sleep(15)

logging.warning("Starting camera 2")

camera_detector.start()

time.sleep(15)

logging.warning("Stopping camera 2")

camera_detector.stop()

