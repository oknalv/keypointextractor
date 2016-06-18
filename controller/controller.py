import cv2

from lib.errors import *
from lib.imageprocdlib import ImageProcDlib
from lib.observable import Observable
from lib.pointtransformerxml import PointTransformerXML


class Controller(Observable):
    @staticmethod
    def get_completed_percentage(total_frame_num, current_frame_num):
        return float(current_frame_num) * 100.0 / float(total_frame_num)

    def generate_output_file(self,input_image_path, input_video_path, output_file_path):

        if input_image_path is None or input_image_path == "":
            raise EmptyImageFileInputError

        if input_video_path is None or input_video_path == "":
            raise EmptyVideoFileInputError

        if output_file_path is None or output_file_path == "":
            raise EmptyFileOutputError

        predictor_path = "resources/shape_predictor_68_face_landmarks.dat"
        image_processor = ImageProcDlib(predictor_path)
        transformer = PointTransformerXML()
        image_file = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
        if image_file is None:
            raise Exception

        image_string = transformer.img2text(image_processor.get_keypoints(image_file))
        video_input_file = cv2.VideoCapture(input_video_path)
        fps = video_input_file.get(cv2.cv.CV_CAP_PROP_FPS) or 24
        frames = []
        current = 0
        percentage = 0
        previous_percentage = 0
        frame_num = 0
        if self.observers:
            while video_input_file.isOpened():
                ret, frame = video_input_file.read()
                if frame is None:
                    break

                frame_num += 1

            video_input_file.release()
            video_input_file = cv2.VideoCapture(input_video_path)

        while video_input_file.isOpened():
            if self.observers:
                previous_percentage = percentage
                percentage = round(self.get_completed_percentage(frame_num, current))
                if previous_percentage != percentage:
                    self.notify_observers(int(percentage))

            current += 1
            ret, frame = video_input_file.read()
            if frame is None:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = image_processor.get_keypoints(gray_frame)
            frames.append(faces)

        video_input_file.release()
        if len(frames) == 0:
            raise Exception

        output_file = open(output_file_path, "w")
        video = transformer.vid2text(frames)
        output_file.write("<file><metadata><fps value='" + str(fps) + "'/></metadata><initial>" + image_string + "</initial>" + video + "</file>")
        output_file.close()
