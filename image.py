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

        self.label = QtWidgets.QLabel()
        self.set_image()
        layout.addWidget(self.label)

        self.setLayout(layout)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_image)
        timer.setInterval(1000)
        timer.start()

        self.showFullScreen()

    def set_image(self):
        images = [f for f in os.listdir() if '.jpg' in f]

        image = images[randrange(0, len(images))]

        screen_resolution = app.desktop().screenGeometry()

        pixmap = QPixmap(image)
        pm = pixmap.scaled(
            screen_resolution.width(), screen_resolution.height(),
            Qt.KeepAspectRatio)
        self.label.setPixmap(pm)

        def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Escape:
                self.close()
            return super().keyPressEvent(event)

        def eventFilter(self, event):
            if event.type() == QtCore.QEvent.KeyPress:
                return True # means stop event propagation
            else:
                return QtWidgets.QDialog.eventFilter(self, event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        #app.main_window = self

        self.title = 'PyQt5 image'
        self.left = 10
        self.top = 10
        self.width = 1920
        self.height = 1080
        self.initUI()

    def initUI(self):
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.buildMenu()

        hbox = QtWidgets.QHBoxLayout()

        left = QtWidgets.QFrame()
        left.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.vbox = QtWidgets.QVBoxLayout()
        self.setImage()
        left.setLayout(self.vbox)

        right = QtWidgets.QFrame()
        right.setFrameShape(QtWidgets.QFrame.StyledPanel)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        hbox.addWidget(splitter)

        screen_resolution = app.desktop().screenGeometry()

        #timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.setImage)
        #timer.setInterval(1000)
        #timer.start()

        main_widget.setLayout(hbox)

        self.show()
        #self.showFullScreen()

    def buildMenu(self):
        exitAction = QtWidgets.QAction(QtGui.QIcon('exit24.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        run = menubar.addMenu('Run')

        slide_show_action = QtWidgets.QAction('Slide Show', self)
        slide_show_action.setShortcut('Ctrl+R')
        slide_show_action.setStatusTip('Start Slideshow')
        slide_show_action.triggered.connect(self.start_slide_show)
        run.addAction(slide_show_action)

    def start_slide_show(self):
        window = SlideShowWindow(self)
        window.exec_()

    def setImage(self):
        images = [f for f in os.listdir() if '.jpg' in f]

        for image in images:
            label = QLabel()
            pixmap = QPixmap(image)
            pm = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
            label.setPixmap(pm)
            self.vbox.addWidget(label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
