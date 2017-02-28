from PyQt5 import QtCore

from django.conf import settings
from django.core.servers.basehttp import run
from django.core.wsgi import get_wsgi_application

from .settings import django_settings


class WebServer(QtCore.QObject):
    @QtCore.pyqtSlot()
    def run(self):
        settings.configure(**django_settings)
        application = get_wsgi_application()
        run('127.0.0.1', 8080, application)
