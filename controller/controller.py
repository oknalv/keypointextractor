from lib.imageprocdlib import ImageProcDlib
from lib.pointtransformerxml import PointTransformerXML
from lib.errors import *
import cv2

def generate(inputimage, inputvideo, outputfile, observer = None):
    def get_percent(total, current):
        return float(current) * 100.0 / float(total)

    if inputimage is None or inputimage == "":
        raise EmptyImageFileInputError

    if inputvideo is None or inputvideo == "":
        raise EmptyVideoFileInputError

    if outputfile is None or outputfile == "":
        raise EmptyFileOutputError

    predictor_path = "resources/shape_predictor_68_face_landmarks.dat"
    imgproc = ImageProcDlib(predictor_path)
    transformer = PointTransformerXML()
    imgFile = cv2.imread(inputimage, cv2.IMREAD_GRAYSCALE)
    if imgFile is None:
        raise Exception

    image = transformer.img2text(imgproc.get_keypoints(imgFile))
    vc = cv2.VideoCapture(inputvideo)
    fps = vc.get(cv2.cv.CV_CAP_PROP_FPS) or 24
    frames = []
    current = 0
    perc = 0
    prev_perc = 0
    frame_num = 0
    if observer is not None:
        while vc.isOpened():
            ret, frame = vc.read()
            if frame == None:
                break
            frame_num += 1

        vc.release()
        vc = cv2.VideoCapture(inputvideo)

    while vc.isOpened():
        if observer is not None:
            prev_perc = perc
            perc = round(get_percent(frame_num, current))
            if prev_perc != perc:
                observer.update_percentage(int(perc))

        current += 1
        ret, frame = vc.read()
        if frame == None:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = imgproc.get_keypoints(img)
        frames.append(faces)

    vc.release()
    if len(frames) == 0:
        raise Exception

    f = open(outputfile, "w")
    video = transformer.vid2text(frames)
    f.write("<file><metadata><fps>" + str(fps) + "</fps></metadata><initial>" + image + "</initial>" + video + "</file>")
    f.close()