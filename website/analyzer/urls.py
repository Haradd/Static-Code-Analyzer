from django.conf.urls import url

from . import views

app_name = 'analyzer'
urlpatterns = [
    url(r'^$', views.upload_form, name='home'),
    url(r'^reports$', views.reports, name='reports'),
    url(r'^upload$', views.upload_form, name='upload'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.logout_user, name='logout'),
    url(r'^register$', views.register_user, name='register'),

]