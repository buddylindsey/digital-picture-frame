import sys
import os
from random import randrange
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QPoint, Qt


app = QApplication.instance()


class SlideShowWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

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
        self.image_location_text = QtWidgets.QLineEdit(self.settings.value('images/location'))

        layout.addWidget(image_location_label)
        layout.addWidget(self.image_location_text)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        layout.addWidget(button_box)
        self.setLayout(layout)

        button_box.accepted.connect(self.save)
        button_box.rejected.connect(self.reject)

    def save(self):
        self.settings.setValue('images/location', self.image_location_text.text())
        del self.settings
        self.accept()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        self.setWindowTitle('Digital Picture Frame')
        self.setGeometry(10, 10, 1920, 1080)
        self.buildMenu()

        hbox = QtWidgets.QHBoxLayout()

        scroll_container = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.set_image()
        scroll_container.setLayout(self.vbox)

        left = QtWidgets.QScrollArea()
        left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        left.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        left.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        left.setWidgetResizable(False)
        left.setWidget(scroll_container)

        right = QtWidgets.QFrame()
        right.setFrameShape(QtWidgets.QFrame.StyledPanel)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        hbox.addWidget(splitter)

        screen_resolution = app.desktop().screenGeometry()

        main_widget.setLayout(hbox)

        self.show()

    def buildMenu(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        settings_action = QtWidgets.QAction('Settings', self)
        settings_action.triggered.connect(self.open_settings)
        fileMenu.addAction(settings_action)

        fileMenu.addSeparator()

        exit_action = QtWidgets.QAction(QtGui.QIcon('exit24.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        fileMenu.addAction(exit_action)

        run = menubar.addMenu('Run')

        slide_show_action = QtWidgets.QAction('Slide Show', self)
        slide_show_action.setShortcut('Ctrl+R')
        slide_show_action.setStatusTip('Start Slideshow')
        slide_show_action.triggered.connect(self.start_slide_show)
        run.addAction(slide_show_action)

    def start_slide_show(self):
        window = SlideShowWindow(self)
        window.exec_()

    def open_settings(self):
        window = SettingsDialog(self)
        if window.exec_():
            self.set_image()

    def set_image(self):
        settings = QtCore.QSettings('digitalframe', 'digitalframe')
        path = settings.value('images/location')
        images = ["{}/{}".format(path, f) for f in os.listdir(path) if '.jpg' in f]

        for image in images:
            image = ImageDisplayWidget(image)
            self.vbox.addWidget(image)


class ImageDisplayWidget(QLabel):
    width = None
    height = None
    image = None

    def __init__(self, image_path, width=200, height=200):
        super().__init__()
        self.image = image_path
        self.width = width
        self.height = height
        self.change_image(self.get_image())

    def change_image(self, image, width=None, height=None):
        self.image = image
        pixmap = QPixmap(self.image)
        pm = pixmap.scaled(
                width or self.width, height or self.height,
                Qt.KeepAspectRatioByExpanding)
        self.setPixmap(pm)

    def get_image(self):
        if self.image:
            return self.image

        raise Exception('No Image available')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
