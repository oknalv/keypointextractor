# coding: utf-8

import xml.etree.ElementTree as xml
import controller.controller as controller
from lib.errors import *
from PyQt4 import QtGui, QtCore

class GUI(QtGui.QWidget):

    def __init__(self):
        super(GUI, self).__init__()
        self.texts = {}
        self.langs = {}
        langxml = xml.parse("resources/lang.xml").getroot()
        for lang in langxml.findall("lang"):
            id = lang.get("id")
            self.texts[id] = []
            self.langs[id] = lang.get("name")
            for text in lang.iter("text"):
                self.texts[id].append(text.text)

        self.init_ui()

    def init_ui(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        optionhbox = QtGui.QHBoxLayout()
        vbox.addLayout(optionhbox)
        langhbox = QtGui.QHBoxLayout()
        optionhbox.addLayout(langhbox)
        langhbox.setAlignment(QtCore.Qt.AlignLeft)
        self.languageLabel = QtGui.QLabel()
        langhbox.addWidget(self.languageLabel)
        self.languageLabel.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.languageCombo = QtGui.QComboBox()
        langhbox.addWidget(self.languageCombo)
        self.languageCombo.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        for lang in sorted(self.langs):
            self.languageCombo.addItem(self.langs[lang])

        self.languageCombo.setCurrentIndex(self.languageCombo.findText("English"))
        self.languageCombo.currentIndexChanged.connect(self.change_language)

        helphbox = QtGui.QHBoxLayout()
        helphbox.setAlignment(QtCore.Qt.AlignRight)
        optionhbox.addLayout(helphbox)
        # self.helpButton = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap("resources/help.png")), "")
        self.helpButton = QtGui.QPushButton(QtGui.QIcon.fromTheme("system-help", QtGui.QIcon("resources/help.png")), "")
        helphbox.addWidget(self.helpButton)
        self.helpButton.clicked.connect(self.show_help)

        inputimagefilehbox = QtGui.QHBoxLayout()
        vbox.addLayout(inputimagefilehbox)
        self.fileInputImageText = QtGui.QLineEdit()
        inputimagefilehbox.addWidget(self.fileInputImageText)
        self.fileInputImageButton = QtGui.QPushButton()
        inputimagefilehbox.addWidget(self.fileInputImageButton)
        self.fileInputImageButton.clicked.connect(self.get_input_image_file)

        inputvideofilehbox = QtGui.QHBoxLayout()
        vbox.addLayout(inputvideofilehbox)
        self.fileInputVideoText = QtGui.QLineEdit()
        inputvideofilehbox.addWidget(self.fileInputVideoText)
        self.fileInputVideoButton = QtGui.QPushButton()
        inputvideofilehbox.addWidget(self.fileInputVideoButton)
        self.fileInputVideoButton.clicked.connect(self.get_input_video_file)

        outputfilehbox = QtGui.QHBoxLayout()
        vbox.addLayout(outputfilehbox)
        self.fileOutputText = QtGui.QLineEdit()
        outputfilehbox.addWidget(self.fileOutputText)
        self.fileOutputButton = QtGui.QPushButton()
        outputfilehbox.addWidget(self.fileOutputButton)
        self.fileOutputButton.clicked.connect(self.get_output_file)

        buttonhbox = QtGui.QHBoxLayout()
        vbox.addLayout(buttonhbox)
        self.generateButton = QtGui.QPushButton()
        buttonhbox.addWidget(self.generateButton)
        self.generateButton.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        buttonhbox.setAlignment(QtCore.Qt.AlignRight)
        self.generateButton.clicked.connect(self.generate)


        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Keypoint extractor")
        self.change_language()
        icon = QtGui.QIcon('resources/logo.png')
        self.setWindowIcon(icon)
        self.show()
        self.setFixedSize(500, self.geometry().height())

    def change_language(self):
        lang = self.get_lang()
        self.languageLabel.setText(self.texts[lang][0])
        self.fileInputVideoButton.setText(self.texts[lang][2])
        self.fileInputImageButton.setText(self.texts[lang][10])
        self.fileOutputButton.setText(self.texts[lang][3])
        self.generateButton.setText(self.texts[lang][1])
        self.helpButton.setText(self.texts[lang][12])

    def show_help(self):
        lang = self.get_lang()
        QtGui.QMessageBox.information(self, self.windowTitle(), self.texts[lang][13], self.texts[lang][6])

    def get_input_image_file(self):
        file = QtGui.QFileDialog.getOpenFileName()
        self.fileInputImageText.setText(file)

    def get_input_video_file(self):
        file = QtGui.QFileDialog.getOpenFileName()
        self.fileInputVideoText.setText(file)

    def get_output_file(self):
        filedialog = QtGui.QFileDialog()
        file = str(filedialog.getSaveFileName(filter = 'XML (*.xml)'))
        if file != "" and not file.endswith(".xml"):
            file += ".xml"
        self.fileOutputText.setText(file)

    def generate(self):
        lang = self.get_lang()
        self.progress = QtGui.QProgressDialog(self.texts[lang][4], "Cancel", 0, 100, self)
        self.progress.setCancelButton(None)
        self.progress.setWindowTitle(self.windowTitle())
        try:
            controller.generate(str(self.fileInputImageText.text()), str(self.fileInputVideoText.text()), str(self.fileOutputText.text()), self)
            QtGui.QMessageBox.information(self, self.windowTitle(), self.texts[lang][5], self.texts[lang][6])

        except EmptyImageFileInputError:
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[lang][11], self.texts[lang][6])

        except EmptyVideoFileInputError:
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[lang][7], self.texts[lang][6])

        except EmptyFileOutputError:
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[lang][8], self.texts[lang][6])

        except Exception, e:
            print(type(e).__name__ + ": " + e.message)
            QtGui.QMessageBox.warning(self, self.windowTitle(), self.texts[lang][9], self.texts[lang][6])


    def update_percentage(self, percentage):
        self.progress.setValue(percentage)

    def get_lang(self):
        lang = "en"
        for l in self.langs:
            if unicode(self.langs[l]) == unicode(self.languageCombo.currentText()):
                lang = l
                break
        return lang