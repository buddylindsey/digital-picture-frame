from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class ImageDisplayWidget(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)
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
        pixmap = QtGui.QPixmap(self.image)
        pm = pixmap.scaled(
                width or self.width, height or self.height,
                QtCore.Qt.KeepAspectRatioByExpanding)
        self.setPixmap(pm)

    def get_image(self):
        if self.image:
            return self.image

        raise Exception('No Image available')

    def mouseReleaseEvent(self, event):
        self.clicked.emit(self.get_image())
        super().mouseReleaseEvent(event)


