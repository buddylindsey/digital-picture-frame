from django.conf.urls import url

from .views import ImageFormView

urlpatterns = (
    url(r'^$', ImageFormView.as_view(), name='upload_image'),
)