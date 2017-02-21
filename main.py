import sys
from PyQt5 import QtWidgets

from src.application import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
