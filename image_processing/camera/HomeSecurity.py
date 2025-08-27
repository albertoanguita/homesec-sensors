import logging
import logging.config
import os
import pickle
import threading
import time

import cv2
import numpy as np
from jacpy.geometry import geoUtils
from jacpy.jthread.ThreadSafe import ThreadSafe
from jacpy.object.Singleton import Singleton
from jacpy.str.strUtils import print_formatted_dict
from jacpy.time.TimedSampleStore import TimedSampleStore
from mtcnn import mtcnn

from image_processing.ImageEvents import ImageEventInterface
from image_processing.model import HumansModel
from FaceEncoder import FaceEncoder
from config.Config import PathsConfig

# The HomeSecurity system is designed to video monitor the entrance of a home and detect if an intruder (not
# registered in the system) is pictured. To do so, the system uses an attached web-cam and two different NNs.
# - HumanDetector: detects if there is a human in the frame. This is a relatively lightweight calculation, so it
# can be run continuously
# - FaceRecognizer: searches for faces in the frame and tries to match them against a set of registered faces. If
# the face is registered, there everything is ok. If there is no face found, or the found face does not match
# against any the registered ones, then and intrusion alarm is fired off, triggering the necessary notifications.




# encodings_path = '../../encodings/encodings.pkl'
# encodings_weights = 'facenet_keras_weights.h5'

required_size = (160, 160)
human_threshold = 5.0
face_threshold = 0.99
recognition_threshold = 0.20



class CameraDetector(Singleton):
    def __init__(self):

        self.running = ThreadSafe(False)
        self.image_events = None
        self.main_loop_thread = None
        self.latest_frame = ThreadSafe(None)

        print(os.path.abspath('logging.ini'))
        logging.config.fileConfig('logging.ini', encoding='UTF-8')

        logger = logging.getLogger('test')
        logger.debug('This is debug message')
        logger.info('This is info message')
        logger.warning('This is warning message')
        logger.error('This is error message')
        logger.critical('This is critical message')

        # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        # logger = logging.getLogger(__name__)
        # logger.setLevel(logging.DEBUG)
        #
        # logger.info("Starting system")

        cwd = os.getcwd()

        config = PathsConfig()
        facenetWeights = config.facenet_weights()
        facesPath = config.faces_path()
        encodingsPath = config.encodings_path()

        logging.info("Config file read. ")
        logging.info(print_formatted_dict(config, value_printer=print_formatted_dict))

        self.human_model = self._load_human_model()
        face_detector = mtcnn.MTCNN()
        self.face_encoder = FaceEncoder(face_detector, facenetWeights, encodingsPath, facesPath)
        if not os.path.isfile(encodingsPath) or self.face_encoder.HasNewSamples():
            self.face_encoder.GenerateEncodings()

        self.face_encoder.LoadEncodings()

        self.initialized = True

        # main_loop(self, self.humanModel, self.face_encoder)


    def initialize(self, image_events: ImageEventInterface):
        if self.image_events is None:
            self.image_events = image_events
            self.image_events.initialized()
        return self

    def start(self):
        if not self.running.get_and_set(True):
            # create camera thread
            self.main_loop_thread = threading.Thread(target=main_loop, args=(self, self.human_model, self.face_encoder))
            self.main_loop_thread.start()


    def stop(self):
        if self.running.get_and_set(False):
            self.main_loop_thread.join()


    def known_person_detected(self):
        self.image_events.known_person()


    def unknown_person_detected(self):
        self.image_events.unknown_person()

    @staticmethod
    def _load_human_model():
        human_model = HumansModel.HumansModel()
        human_model.load_weights('weights/detect_humans_weight_IV2.h5')
        logging.info("Human model loaded correctly")
        return human_model

    # def load_pickle(self, path):
    #     with open(path, 'rb') as f:
    #         encoding_dict = pickle.load(f)
    #     return encoding_dict

    @staticmethod
    def divide(frame: cv2.typing.MatLike):
        shape = frame.shape
        rows = shape[0]
        cols = shape[1]
        partitions = geoUtils.partition2DGeometry(cols, rows, 320, 320, 0.2, growRatio=1.5)
        return partitions

    @staticmethod
    def detect_humans(img: cv2.typing.MatLike, partitions, humanModel):
        # humanParts = []
        # noHumanParts = []
        # partsWithColor = []
        partitioned_images = list(map(lambda p : img[p[0][1]:p[1][1], p[0][0]:p[1][0]], partitions))
        processed_images = np.array(list(map(lambda i : cv2.resize(i, required_size), partitioned_images)))
        human_predictions = humanModel.predict(processed_images)
        human_prediction = max(human_predictions)

        return human_prediction > human_threshold, human_prediction[0]


    @staticmethod
    def detect_faces(frame, img, encoder):
        known, unknown = encoder.DetectFaces(img, face_threshold, recognition_threshold)

        has_known_person = any(known)

        for aKnown in known:
            name = aKnown[0]
            distance = aKnown[1]
            pt_1 = aKnown[2]
            pt_2 = aKnown[3]
            cv2.rectangle(frame, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(frame, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 200, 200), 2)

        for anUnknown in unknown:
            pt_1 = anUnknown[0]
            pt_2 = anUnknown[1]
            cv2.rectangle(frame, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(frame, 'unknown', pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        return frame, has_known_person

    # def get_face(self, img, box):
    #     x1, y1, width, height = box
    #     x1, y1 = abs(x1), abs(y1)
    #     x2, y2 = x1 + width, y1 + height
    #     face = img[y1:y2, x1:x2]
    #     return face, (x1, y1), (x2, y2)


    @staticmethod
    def add_fps(frame, timed_store, has_human, human_thr):
        fps = timed_store.count() / 5.0
        color = (255, 0, 0) if has_human else (0, 255, 0)
        cv2.putText(frame, f'{str(fps)} / {str(human_thr)}', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        return frame



def main_loop(camera_detector: CameraDetector, human_model, face_encoder):
    logging.info("Initiating main loop")
    cap = cv2.VideoCapture(0)
    logging.info("Video capture initiated")
    frame_count = 0
    timed_store = TimedSampleStore(5000)

    while camera_detector.running.get() and cap.isOpened():
        success, frame = cap.read()

        if not success:
            logging.error("Camera is not accessible. Exiting program!!!")
            break

        logging.debug("Processing a new frame")
        timed_store.add(True)

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        camera_detector.latest_frame.set(img_rgb)
        partitions = CameraDetector.divide(frame)

        human_detected, human_thr = CameraDetector.detect_humans(img_rgb, partitions, human_model)
        if human_detected:
            logging.warning(f"Human detected in frame {frame_count}")
            # frame = detect.detect(frame, face_detector, face_encoder, encoding_dict)
            frame, has_known_person = CameraDetector.detect_faces(frame, img_rgb, face_encoder)

            if has_known_person:
                camera_detector.known_person_detected()
            else:
                camera_detector.unknown_person_detected()

            has_human = True
        else:
            logging.debug(f'No human detected in frame {frame_count}')
            has_human = False

        frame = CameraDetector.add_fps(frame, timed_store, has_human, human_thr)

        logging.debug(f'Drawing frame {frame_count}...')
        cv2.imshow('camera', frame)
        logging.debug(f'Draw frame {frame_count}')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    logging.debug(f'Ending video capture {frame_count}...')
    cap.release()
    cv2.destroyAllWindows()
