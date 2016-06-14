import dlib
from imageproc import ImageProc


class ImageProcDlib(ImageProc):
    def __init__(self, predictor_path):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

    def get_keypoints(self, img):
        face_detections = self.detector(img, 1)
        keypoints = []
        for face in face_detections:
            points = self.predictor(img, face)
            keypoints.append([[point.x, point.y] for point in points.parts()])

        return keypoints
