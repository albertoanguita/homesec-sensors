import configparser
import logging
import logging.config
import os
import pickle

import cv2
import numpy as np
from jacpy.geometry import geoUtils
from jacpy.time.TimedSampleStore import TimedSampleStore
from mtcnn import mtcnn

import HumansModel
from FaceEncoder import FaceEncoder

# The HomeSecurity system is designed to video monitor the entrance of a home and detect if an intruder (not
# registered in the system) is pictured. To do so, the system uses an attached web-cam and two different NNs.
# - HumanDetector: detects if there is a human in the frame. This is a relatively lightweight calculation, so it
# can be run continuously
# - FaceRecognizer: searches for faces in the frame and tries to match them against a set of registered faces. If
# the face is registered, there everything is ok. If there is no face found, or the found face does not match
# against any the registered ones, then and intrusion alarm is fired off, triggering the necessary notifications.


timedStore = TimedSampleStore(5000)

encodings_path = 'encodings/encodings.pkl'
encodings_weights = 'facenet_keras_weights.h5'

required_size = (160, 160)
human_threshold = 5.0
face_threshold = 0.99
recognition_threshold = 0.20


def init():
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

    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['CONFIG']
    facenetWeights = config['facenetWeights']
    facesPath = config['facesPath']
    encodingsPath = config['encodingsPath']

    logging.info("Config file read. ")
    for item in config.items():
        logging.info(f"  {item[0]}: {item[1]}")

    humanModel = loadHumanModel()
    face_detector = mtcnn.MTCNN()
    face_encoder = FaceEncoder(face_detector, facenetWeights, encodingsPath, facesPath)
    if not os.path.isfile(encodingsPath) or face_encoder.HasNewSamples():
        face_encoder.GenerateEncodings()

    face_encoder.LoadEncodings()

    mainLoop(humanModel, face_encoder)

def loadHumanModel():
    humanModel = HumansModel.HumansModel()
    humanModel.load_weights('weights/detect_humans_weight_IV2.h5')
    logging.info("Human model loaded correctly")
    return humanModel

def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict

def divide(frame: cv2.typing.MatLike):
    shape = frame.shape
    rows = shape[0]
    cols = shape[1]
    partitions = geoUtils.partition2DGeometry(cols, rows, 320, 320, 0.2, growRatio=1.5)
    return partitions

def detectHumans(img: cv2.typing.MatLike, partitions, humanModel):
    # humanParts = []
    # noHumanParts = []
    # partsWithColor = []
    partitionedImages = list(map(lambda p : img[p[0][1]:p[1][1], p[0][0]:p[1][0]], partitions))
    processedImages = np.array(list(map(lambda i : cv2.resize(i, required_size), partitionedImages)))
    humanPredictions = humanModel.predict(processedImages)
    humanPrediction = max(humanPredictions)

    return humanPrediction > human_threshold, humanPrediction[0]


def detectFaces(frame, img, encoder):
    known, unknown = encoder.DetectFaces(img, face_threshold, recognition_threshold)

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
    return frame

def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)


def addFps(frame, timedStore, hasHuman, human_thr):
    fps = timedStore.count() / 5.0
    color = (255, 0, 0) if hasHuman else (0, 255, 0)
    cv2.putText(frame, f'{str(fps)} / {str(human_thr)}', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return frame


def mainLoop(humanModel, face_encoder):
    logging.info("Initiating main loop")
    cap = cv2.VideoCapture(0)
    logging.info("Video capture initiated")
    frame_count = 0

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            logging.error("Camera is not accessible. Exiting program!!!")
            break

        logging.debug("Processing a new frame")
        timedStore.add(True)

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        partitions = divide(frame)

        human_detected, human_thr = detectHumans(img_rgb, partitions, humanModel)
        if (human_detected):
            logging.warning(f"Human detected in frame {frame_count}")
            # frame = detect.detect(frame, face_detector, face_encoder, encoding_dict)
            frame = detectFaces(frame, img_rgb, face_encoder)
            hasHuman = True
        else:
            logging.debug(f'No human detected in frame {frame_count}')
            hasHuman = False

        frame = addFps(frame, timedStore, hasHuman, human_thr)

        cv2.imshow('camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1



init()