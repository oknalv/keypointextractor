import controller.controller as controller
from lib.errors import *
import sys


class CLI:
    def __init__(self):
        print "Keypoint extractor"

    def get_files(self):
        input_image_file = raw_input("Input image file: ")
        input_video_file = raw_input("Input video file: ")
        output_file = raw_input("Output file: ")
        self.generate_output_file(input_image_file, input_video_file, output_file)

    def generate_output_file(self, input_image_file, input_video_file, output_file):
        try:
            controller.generate_output_file(input_image_file, input_video_file, output_file, self)
            print "\nFile successfully created"

        except EmptyImageFileInputError:
            print "You didn't specified an input image file"

        except EmptyVideoFileInputError:
            print "You didn't specified an input video file."

        except EmptyFileOutputError:
            print "You didn't specified an output file."

        except:
            print "An unexpected error occurred. File could not be created."

    def update_completed_percentage(self, percentage):
        sys.stdout.write('\r' + str(percentage) + "%")
        sys.stdout.flush()
