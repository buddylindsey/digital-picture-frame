from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class ImageDisplayWidget(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)
    width = None
    height = None
    image = None
    currentQRubberBand = None

    def __init__(self, image_path, width=200, height=200, editable=False):
        super().__init__()
        self.image = QtGui.QImage(image_path)
        self.width = width
        self.height = height
        self.change_image(self.get_image())

    def change_image(self, image, width=None, height=None):
        if isinstance(image, QtGui.QImage):
            self.image = image
        else:
            self.image = QtGui.QImage(image)
        pixmap = QtGui.QPixmap.fromImage(self.image)
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

    def mousePressEvent(self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        if not self.currentQRubberBand:
            self.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
            self.currentQRubberBand.setGeometry(200, 200, 200, 200)
            self.currentQRubberBand.show()
        super().mousePressEvent(eventQMouseEvent)

    def mouseMoveEvent (self, eventQMouseEvent):
        if self.currentQRubberBand:
            self.currentQRubberBand.move(eventQMouseEvent.pos())
        super().mouseMoveEvent(eventQMouseEvent)

