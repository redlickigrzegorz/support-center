from django.conf.urls import url
from . import views, views_json


app_name = 'cti'
urlpatterns = [
    #login
    url(r'^$', views.login, name='login'),
    url(r'^json/login/$', views_json.login, name='login_json'),

    #logout
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^json/logout/$', views_json.logout, name='logout_json'),

    #index
    url(r'^index/$', views.index, name='index'),
    url(r'^json/index/$', views_json.index, name='index_json'),

    #my faults
    url(r'^my_faults/$', views.my_faults, name='my_faults'),
    url(r'^json/my_faults/$', views_json.my_faults, name='my_faults_json'),



    url(r'^logout/$', views.logout, name='logout'),

    url(r'^detail/(?P<fault_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add_fault, name='add_fault'),
    url(r'^edit/(?P<fault_id>[0-9]+)/$', views.edit_fault, name='edit_fault'),
    url(r'^delete/(?P<fault_id>[0-9]+)/$', views.delete_fault, name='delete_fault'),
    url(r'^assign_to_me/(?P<fault_id>[0-9]+)/$', views.assign_to_me, name='assign_to_me'),
    url(r'^resolved_faults/$', views.resolved_faults, name='resolved_faults'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    # mobile views


    url(r'^detail_mobile/(?P<fault_id>[0-9]+)/$', views_json.detail_mobile, name='detail_mobile'),
    url(r'^add_fault_mobile/$', views_json.add_fault_mobile, name='add_fault_mobile'),
    url(r'^edit_fault_mobile/(?P<fault_id>[0-9]+)/$', views_json.edit_fault_mobile, name='edit_fault_mobile'),
    url(r'^delete_fault_mobile/(?P<fault_id>[0-9]+)/$', views_json.delete_fault_mobile, name='delete_fault_mobile'),
    url(r'^assign_fault_mobile/(?P<fault_id>[0-9]+)/$', views_json.assign_to_me_mobile, name='assign_to_me_mobilei'),
    url(r'^resolved_faults_mobile/$', views_json.resolved_faults_mobile, name='resolved_faults_mobile'),
    url(r'^test/$', views_json.test, name='test'),
]
