import controller.controller as controller
from lib.errors import *
import sys

class CLI:

    def __init__(self):
        print "Keypoint extractor"

    def get_files(self):
        inputimagefile = raw_input("Input image file: ")
        inputvideofile = raw_input("Input video file: ")
        outputfile = raw_input("Output file: ")
        self.generate(inputimagefile, inputvideofile, outputfile)

    def generate(self,inputimagefile, inputvideofile, outputfile):
        try:
            controller.generate(inputimagefile, inputvideofile, outputfile, self)
            print "\nFile succesfully created"

        except EmptyImageFileInputError:
            print "You didn't specified an input image file"

        except EmptyVideoFileInputError:
            print "You didn't specified an input video file."

        except EmptyFileOutputError:
            print "You didn't specified an output file."

        except:
            print "An unexpected error occurred. File could not be created."

    def update_percentage(self, percentage):
        sys.stdout.write('\r' + str(percentage) + "%")
        sys.stdout.flush()