import os
import sys
from PyQt5 import QtCore

from django.conf import settings
from django.core.servers.basehttp import run, get_internal_wsgi_application
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

DEBUG = True
SECRET_KEY = os.urandom(32)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

def index(request):
    return HttpResponse('Hello World')

urlpatterns = (
    url(r'^$', index),
)

application = get_wsgi_application()


class WebServer(QtCore.QObject):
    @QtCore.pyqtSlot()
    def run(self):
        run('127.0.0.1', 8080, application)
