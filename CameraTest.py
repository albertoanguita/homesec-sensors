import time
import logging

from image_processing.camera.HomeSecurity import CameraDetector

camera_detector = CameraDetector()

time.sleep(5)

logging.info("Starting camera")

camera_detector.start()

time.sleep(15)

logging.info("Stopping camera")

camera_detector.stop()

time.sleep(15)

logging.info("Starting camera")

camera_detector.start()

time.sleep(15)

logging.info("Stopping camera")

camera_detector.stop()

