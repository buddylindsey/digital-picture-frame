import os
import sys
from PyQt5 import QtCore, QtWidgets

from django import forms
from django.conf import settings
from django.core.servers.basehttp import run, get_internal_wsgi_application
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

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
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['{}'.format(os.path.dirname(os.path.abspath(__file__)))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },]
)


class ImageForm(forms.Form):
    image = forms.FileField(label='Select an Image to upload')


def handle_uploaded_file(f):
    settings = QtCore.QSettings('digitalframe', 'digitalframe')
    path = settings.value('images/location')
    with open('{}/{}'.format(path, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['image'])
            return HttpResponseRedirect('/')
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})


urlpatterns = (
    url(r'^$', index),
)

application = get_wsgi_application()


class WebServer(QtCore.QObject):
    @QtCore.pyqtSlot()
    def run(self):
        run('127.0.0.1', 8080, application)
