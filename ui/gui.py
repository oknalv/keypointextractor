# coding: utf-8

import xml.etree.ElementTree as xml
from controller.controller import Controller
from lib.errors import *
from lib.observer import Observer
from PyQt4 import QtGui, QtCore


class GUI(QtGui.QWidget, Observer):
    def __init__(self):
        super(GUI, self).__init__()
        self.texts = {}
        self.languages = {}
        languages_xml_file = xml.parse("resources/lang.xml").getroot()
        for lang in languages_xml_file.findall("lang"):
            id = lang.get("id")
            self.texts[id] = []
            self.languages[id] = lang.get("name")
            for text in lang.iter("text"):
                self.texts[id].append(text.text)

        self.init_ui()

    def init_ui(self):
        vertical_box = QtGui.QVBoxLayout()
        self.setLayout(vertical_box)

        options_horizontal_box = QtGui.QHBoxLayout()
        vertical_box.addLayout(options_horizontal_box)
        languages_horizontal_box = QtGui.QHBoxLayout()
        options_horizontal_box.addLayout(languages_horizontal_box)
        languages_horizontal_box.setAlignment(QtCore.Qt.AlignLeft)
        self.language_label = QtGui.QLabel()
        languages_horizontal_box.addWidget(self.language_label)
        self.language_label.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.language_combo = QtGui.QComboBox()
        languages_horizontal_box.addWidget(self.language_combo)
        self.language_combo.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        for language in sorted(self.languages):
            self.language_combo.addItem(self.languages[language])

        self.language_combo.setCurrentIndex(self.language_combo.findText("English"))
        self.language_combo.currentIndexChanged.connect(self.change_language)

        help_horizontal_box = QtGui.QHBoxLayout()
        help_horizontal_box.setAlignment(QtCore.Qt.AlignRight)
        options_horizontal_box.addLayout(help_horizontal_box)
        self.help_button = QtGui.QPushButton(QtGui.QIcon.fromTheme("system-help", QtGui.QIcon("resources/help.png")), "")
        help_horizontal_box.addWidget(self.help_button)
        self.help_button.clicked.connect(self.show_help)

        input_image_file_horizontal_box = QtGui.QHBoxLayout()
        vertical_box.addLayout(input_image_file_horizontal_box)
        self.file_input_image_text = QtGui.QLineEdit()
        input_image_file_horizontal_box.addWidget(self.file_input_image_text)
        self.file_input_image_button = QtGui.QPushButton()
        input_image_file_horizontal_box.addWidget(self.file_input_image_button)
        self.file_input_image_button.clicked.connect(self.get_input_image_file)

        input_video_file_horizontal_box = QtGui.QHBoxLayout()
        vertical_box.addLayout(input_video_file_horizontal_box)
        self.file_input_video_text = QtGui.QLineEdit()
        input_video_file_horizontal_box.addWidget(self.file_input_video_text)
        self.file_input_video_button = QtGui.QPushButton()
        input_video_file_horizontal_box.addWidget(self.file_input_video_button)
        self.file_input_video_button.clicked.connect(self.get_input_video_file)

        output_file_horizontal_box = QtGui.QHBoxLayout()
        vertical_box.addLayout(output_file_horizontal_box)
        self.file_output_text = QtGui.QLineEdit()
        output_file_horizontal_box.addWidget(self.file_output_text)
        self.file_output_button = QtGui.QPushButton()
        output_file_horizontal_box.addWidget(self.file_output_button)
        self.file_output_button.clicked.connect(self.get_output_file)

        button_horizontal_box = QtGui.QHBoxLayout()
        vertical_box.addLayout(button_horizontal_box)
        self.generate_button = QtGui.QPushButton()
        button_horizontal_box.addWidget(self.generate_button)
        self.generate_button.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        button_horizontal_box.setAlignment(QtCore.Qt.AlignRight)
        self.generate_button.clicked.connect(self.generate_output_file)

        self.setWindowTitle("Keypoint extractor")
        self.change_language()
        icon = QtGui.QIcon('resources/logo.png')
        self.setWindowIcon(icon)
        self.show()
        self.setFixedSize(500, self.geometry().height())

    def change_language(self):
        language = self.get_lang()
        self.language_label.setText(self.texts[language][0])
        self.file_input_video_button.setText(self.texts[language][2])
        self.file_input_image_button.setText(self.texts[language][10])
        self.file_output_button.setText(self.texts[language][3])
        self.generate_button.setText(self.texts[language][1])
        self.help_button.setText(self.texts[language][12])

    def show_help(self):
        language = self.get_lang()
        QtGui.QMessageBox.information(self, self.windowTitle(), self.texts[language][13], self.texts[language][6])

    def get_input_image_file(self):
        file_input_path = QtGui.QFileDialog.getOpenFileName()
        self.file_input_image_text.setText(file_input_path)

    def get_input_video_file(self):
        file_input_path = QtGui.QFileDialog.getOpenFileName()
        self.file_input_video_text.setText(file_input_path)

    def get_output_file(self):
        file_dialog = QtGui.QFileDialog()
        file_output_path = str(file_dialog.getSaveFileName(filter = 'XML (*.xml)'))
        if file_output_path != "" and not file_output_path.endswith(".xml"):
            file_output_path += ".xml"
        self.file_output_text.setText(file_output_path)

    def generate_output_file(self):
        language = self.get_lang()
        self.progress = QtGui.QProgressDialog(self.texts[language][4], "Cancel", 0, 100, self)
        self.progress.setCancelButton(None)
        self.progress.setWindowTitle(self.windowTitle())
        try:
            controller = Controller()
            controller.add_observer(self)
            controller.generate_output_file(str(self.file_input_image_text.text()), str(self.file_input_video_text.text()), str(self.file_output_text.text()))
            QtGui.QMessageBox.information(self, self.windowTitle(), self.texts[language][5], self.texts[language][6])

        except EmptyImageFileInputError:
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[language][11], self.texts[language][6])

        except EmptyVideoFileInputError:
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[language][7], self.texts[language][6])

        except EmptyFileOutputError:
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[language][8], self.texts[language][6])

        except Exception, e:
            print(type(e).__name__ + ": " + e.message)
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[language][9], self.texts[language][6])

    def update(self, percentage):
        self.progress.setValue(percentage)

    def get_lang(self):
        language = "en"
        for l in self.languages:
            if unicode(self.languages[l]) == unicode(self.language_combo.currentText()):
                language = l
                break
        return language
