import sys
import os
from random import randrange
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QPoint, Qt


app = QApplication.instance()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        app.main_window = self

        self.title = 'PyQt5 image'
        self.left = 10
        self.top = 10
        self.width = 1920
        self.height = 1080
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        screen_resolution = app.desktop().screenGeometry()

        self.label = QLabel()
        self.setImage()
        self.setCentralWidget(self.label)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.setImage)
        timer.setInterval(1000)
        timer.start()

        #self.show()
        self.showFullScreen()

    def setImage(self):
        print('set image')
        images = [f for f in os.listdir() if '.jpg' in f]

        image = images[randrange(0, len(images))]

        pixmap = QPixmap(image)
        #pm = pixmap.scaled(1920, 1080, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
