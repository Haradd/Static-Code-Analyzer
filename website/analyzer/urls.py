from django.conf.urls import url

from . import views

app_name = 'analyzer'
urlpatterns = [
    url(r'^$', views.reports, name='reports'),
    url(r'^upload$', views.upload_form, name='upload'),
]