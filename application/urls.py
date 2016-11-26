from django.conf.urls import url
from . import views


app_name = 'application'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<fault_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add$', views.add_fault, name='add_fault'),
]
