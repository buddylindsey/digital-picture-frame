import os

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from .dialogs import SettingsDialog, SlideShowWindow
from .web.server import WebServer
from .widgets import ImageDisplayWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        self.setWindowTitle('Digital Picture Frame')
        self.setGeometry(10, 10, 1920, 1080)
        self.build_menu()

        hbox = QtWidgets.QHBoxLayout()

        scroll_container = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.set_image()
        scroll_container.setLayout(self.vbox)

        left = QtWidgets.QScrollArea()
        left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        left.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        left.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        left.setWidgetResizable(False)
        left.setWidget(scroll_container)

        right = QtWidgets.QFrame()
        self.right_image = ImageDisplayWidget('image.jpg', 1280, 720)
        right_layout = QtWidgets.QHBoxLayout()
        right_layout.addWidget(self.right_image)
        right.setLayout(right_layout)
        right.setFrameShape(QtWidgets.QFrame.StyledPanel)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        hbox.addWidget(splitter)

        main_widget.setLayout(hbox)

        self.show()

        self.thread = QtCore.QThread()
        self.ws = WebServer()
        self.ws.moveToThread(self.thread)

        self.thread.started.connect(self.ws.run)
        self.thread.start()

    @QtCore.pyqtSlot(str)
    def image_selected(self, image):
        self.right_image.change_image(image)

    def build_menu(self):
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
            image.clicked.connect(self.image_selected)
            self.vbox.addWidget(image)

