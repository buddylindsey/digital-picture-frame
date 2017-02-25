from PyQt5 import QtCore

from http.server import HTTPServer, SimpleHTTPRequestHandler

class WebServer(QtCore.QObject):
    @QtCore.pyqtSlot()
    def run(self):
        self._server = HTTPServer(('127.0.0.1', 8080), SimpleHTTPRequestHandler)
        self._server.serve_forever()
