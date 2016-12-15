from django.conf.urls import url
from . import views


app_name = 'cti'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^my_faults/$', views.my_faults, name='my_faults'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^index/$', views.index, name='index'),
    url(r'^detail/(?P<fault_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add_fault, name='add_fault'),
    url(r'^edit/(?P<fault_id>[0-9]+)/$', views.edit_fault, name='edit_fault'),
    url(r'^delete/(?P<fault_id>[0-9]+)/$', views.delete_fault, name='delete_fault')
]
