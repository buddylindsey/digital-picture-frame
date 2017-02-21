import os
import sys
from random import randrange

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

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

        layout = QtWidgets.QVBoxLayout()

        image_location_label = QtWidgets.QLabel('Image Location')
        self.image_location_text = QtWidgets.QLineEdit(
            self.settings.value('images/location'))

        layout.addWidget(image_location_label)
        layout.addWidget(self.image_location_text)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        layout.addWidget(button_box)
        self.setLayout(layout)

        button_box.accepted.connect(self.save)
        button_box.rejected.connect(self.reject)

    def save(self):
        self.settings.setValue(
            'images/location', self.image_location_text.text())
        del self.settings
        self.accept()
