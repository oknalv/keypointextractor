import dlib
from imageproc import ImageProc

class ImageProcDlib(ImageProc):

    def __init__(self, predictor_path):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

    def get_keypoints(self, img):
        dets = self.detector(img, 1)
        elements = []
        for k, d in enumerate(dets):
            parts = self.predictor(img, d)
            elements.append([[p.x, p.y] for p in parts.parts()])

        return elements
