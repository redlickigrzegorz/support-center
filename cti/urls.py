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
    url(r'^delete/(?P<fault_id>[0-9]+)/$', views.delete_fault, name='delete_fault'),
    url(r'^assign_to_me/(?P<fault_id>[0-9]+)/$', views.assign_to_me, name='assign_to_me'),
    url(r'^resolved_faults/$', views.resolved_faults, name='resolved_faults'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^index_mobile/$', views.index_mobile, name='index_mobile'),
    url(r'^login_mobile/$', views.login_mobile, name='login_mobile'),
    url(r'^logout_mobile/$', views.logout_mobile, name='logout_mobile'),
    url(r'^my_faults_mobile/$', views.my_faults_mobile, name='my_faults_mobile'),
    url(r'^detail_mobile/(?P<fault_id>[0-9]+)/$', views.detail_mobile, name='detail_mobile'),
    url(r'^add_fault_mobile/$', views.add_fault_mobile, name='add_fault_mobile'),
    url(r'^edit_fault_mobile/(?P<fault_id>[0-9]+)/$', views.edit_fault_mobile, name='edit_fault_mobile'),
    url(r'^resolved_faults_mobile/$', views.resolved_faults_mobile, name='resolved_faults_mobile'),
]
