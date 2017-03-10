import os
import sys
from random import randrange

from PyQt5 import QtWidgets, QtCore, QtGui

from .widgets import ImageDisplayWidget


class SlideShowWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        app = QtWidgets.QApplication.instance()
        screen_resolution = app.desktop().screenGeometry()

        self.image = ImageDisplayWidget(
            self.get_image(), screen_resolution.width(),
            screen_resolution.height())

        layout.addWidget(self.image)

        self.setLayout(layout)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.change_image)
        timer.setInterval(2000)
        timer.start()

        self.showFullScreen()

    def change_image(self):
        self.image.change_image(self.get_image())

    def get_image(self):
        settings = QtCore.QSettings('digitalframe', 'digitalframe')
        path = settings.value('images/location')
        images = ["{}/{}".format(path, f) for f in os.listdir(path) if '.jpg' in f]

        image = images[randrange(0, len(images))]

        return image

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        return super().keyPressEvent(event)


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings('digitalframe', 'digitalframe')

        # Tab Widgets
        self.tabs = QtWidgets.QTabWidget()
        self.location_tab = QtWidgets.QWidget()
        self.computer_tab = QtWidgets.QWidget()

        # add widgets to tabs and add titles
        self.tabs.addTab(self.location_tab, "Location")
        self.tabs.addTab(self.computer_tab, "Computer")

        # build the UI for each tab
        self.build_location_tab()
        self.build_computer_tab()

        # main layout for dialog
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tabs)
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        self.layout.addWidget(button_box)

        self.setLayout(self.layout)

        # connect methods to buttons
        button_box.accepted.connect(self.save)
        button_box.rejected.connect(self.reject)

    def build_computer_tab(self):
        computer_tab_layout = QtWidgets.QVBoxLayout()
        aspect_ratio_label = QtWidgets.QLabel('Aspect Ratio')
        computer_tab_layout.addWidget(aspect_ratio_label)

        self.aspect_group = QtWidgets.QButtonGroup(computer_tab_layout)

        def add_radio_button(label, ratio):
            row = QtWidgets.QHBoxLayout()
            rb = QtWidgets.QRadioButton(ratio)
            rb.setChecked(ratio == self.settings.value('computer/aspect-ratio'))
            row.addWidget(rb)
            label = QtWidgets.QLabel(label)
            label.setAlignment(QtCore.Qt.AlignRight)
            row.addWidget(label)
            self.aspect_group.addButton(rb)
            computer_tab_layout.addLayout(row)

        add_radio_button("800x600, 1024x768, 1280x960, 2048x1536", "4:3")
        add_radio_button("1920x1080, 3840x2160, 3840x2160, 5120x2880", "16:9")
        add_radio_button("1920x1200", "16:10")

        self.computer_tab.setLayout(computer_tab_layout)

    def build_location_tab(self):
        location_tab_layout = QtWidgets.QVBoxLayout()
        image_location_label = QtWidgets.QLabel('Image Location')
        self.image_location_text = QtWidgets.QLineEdit(self.settings.value('images/location'))

        location_tab_layout.addWidget(image_location_label)
        location_tab_layout.addWidget(self.image_location_text)

        self.location_tab.setLayout(location_tab_layout)

    def save(self):
        self.settings.setValue('images/location', self.image_location_text.text())
        self.settings.setValue('computer/aspect-ratio', self.aspect_group.checkedButton().text())
        del self.settings
        self.accept()
