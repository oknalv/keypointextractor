import sys
from ui.cli import CLI
from ui.gui import GUI
from PyQt4 import QtGui

numargs = len(sys.argv)
if numargs == 1:
    app = QtGui.QApplication(sys.argv)
    w = GUI()
    sys.exit(app.exec_())

elif numargs == 2 and sys.argv[1] == "--console":
    CLI().get_files()

elif numargs == 4:
    CLI().generate(sys.argv[1], sys.argv[2], sys.argv[3])

else:
    print("Usage:\n\tkeypointextractor\n\tkeypointextractor --console\n\tkeypointextractor <input_image_file> <input_video_file> <output_file>")