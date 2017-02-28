from PyQt5 import QtCore

from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView

from .forms import ImageForm


class ImageFormView(FormView):
    form_class = ImageForm
    success_url = reverse_lazy('upload_image')
    template_name = 'templates/image.html'

    def form_valid(self, form):
        self.handle_uploaded_file(self.request.FILES['image'])
        return super().form_valid(form)

    def handle_uploaded_file(self, f):
        settings = QtCore.QSettings('digitalframe', 'digitalframe')
        path = settings.value('images/location')
        with open('{}/{}'.format(path, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
