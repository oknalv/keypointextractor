import sys
from ui.cli import CLI
from ui.gui import GUI
from PyQt4 import QtGui

num_args = len(sys.argv)
if num_args == 1:
    app = QtGui.QApplication(sys.argv)
    w = GUI()
    sys.exit(app.exec_())

elif num_args == 2 and sys.argv[1] == "--console":
    CLI().get_files()

elif num_args == 4:
    CLI().generate_output_file(sys.argv[1], sys.argv[2], sys.argv[3])

else:
    print("Usage:\n\tkeypointextractor\n\tkeypointextractor --console\n\tkeypointextractor <input_image_file> <input_video_file> <output_file>")
