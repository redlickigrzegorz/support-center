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

    #resolved faults
    url(r'^resolved_faults/$', views.resolved_faults, name='resolved_faults'),
    url(r'^json/resolved_faults/$', views_json.resolved_faults, name='resolved_faults_json'),

    #adding fault
    url(r'^add_fault/$', views.add_fault, name='add_fault'),
    url(r'^json/add_fault$', views_json.add_fault, name='add_fault_json'),

    #editing fault
    url(r'^edit_fault/(?P<fault_id>[0-9]+)/$', views.edit_fault, name='edit_fault'),
    url(r'^json/edit_fault/(?P<fault_id>[0-9]+)/$', views_json.edit_fault, name='edit_fault_json'),

    #deleting fault
    url(r'^delete/(?P<fault_id>[0-9]+)/$', views.delete_fault, name='delete_fault'),
    url(r'^json/delete_fault/(?P<fault_id>[0-9]+)/$', views_json.delete_fault, name='delete_fault_json'),

    #details of fault
    url(r'^detail/(?P<fault_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^json/detail/(?P<fault_id>[0-9]+)/$', views_json.detail, name='detail_json'),

    #assigning fault
    url(r'^assign_to_me/(?P<fault_id>[0-9]+)/$', views.assign_to_me, name='assign_to_me'),
    url(r'^json/assign_to_me/(?P<fault_id>[0-9]+)/$', views_json.assign_to_me, name='assign_to_me_json'),

    #changing password
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^json/change_password/$', views_json.change_password, name='change_password_json'),
]
