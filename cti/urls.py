from django.conf.urls import url
from . import views, views_json, views_admin


app_name = 'cti'
urlpatterns = [
    # login
    url(r'^$', views.login, name='login'),
    url(r'^json/login/$', views_json.login, name='login_json'),

    # logout
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^json/logout/$', views_json.logout, name='logout_json'),

    # index
    url(r'^index/$', views.index, name='index'),
    url(r'^json/index/$', views_json.index, name='index_json'),

    # my faults
    url(r'^my_faults/$', views.my_faults, name='my_faults'),
    url(r'^json/my_faults/$', views_json.my_faults, name='my_faults_json'),

    # resolved faults
    url(r'^resolved_faults/$', views.resolved_faults, name='resolved_faults'),
    url(r'^json/resolved_faults/$', views_json.resolved_faults, name='resolved_faults_json'),

    # sorted faults
    url(r'^sorted_faults/(?P<order_by>.+)$', views.sorted_faults, name='sorted_faults'),
    url(r'^json/sorted_faults/(?P<order_by>.+)$', views_json.sorted_faults, name='sorted_faults_json'),

    # searched faults
    url(r'^searched_faults/$', views.searched_faults, name='searched_faults'),

    # adding fault
    url(r'^add_fault/$', views.add_fault, name='add_fault'),
    url(r'^json/add_fault$', views_json.add_fault, name='add_fault_json'),

    # editing fault
    url(r'^edit_fault/(?P<fault_id>[0-9]+)/$', views.edit_fault, name='edit_fault'),
    url(r'^json/edit_fault/(?P<fault_id>[0-9]+)/$', views_json.edit_fault, name='edit_fault_json'),
    url(r'^admin/edit_fault/(?P<fault_id>[0-9]+)/$', views_admin.edit_fault, name='edit_fault_admin'),

    # deleting fault
    url(r'^delete/(?P<fault_id>[0-9]+)/$', views.delete_fault, name='delete_fault'),
    url(r'^json/delete_fault/(?P<fault_id>[0-9]+)/$', views_json.delete_fault, name='delete_fault_json'),

    # details of fault
    url(r'^fault_details/(?P<fault_id>[0-9]+)/$', views.fault_details, name='fault_details'),
    url(r'^json/fault_details/(?P<fault_id>[0-9]+)/$', views_json.fault_details, name='fault_details_json'),

    # details of object
    url(r'^object_details/(?P<object_id>[0-9]+)/$', views.object_details, name='object_details'),
    url(r'^json/object_details/(?P<object_id>[0-9]+)/$', views_json.object_details, name='object_details_json'),

    # details of user
    url(r'^user_details/$', views.user_details, name='user_details'),
    url(r'^json/user_details/$', views_json.user_details, name='user_details_json'),

    # assigning fault
    url(r'^assign_to_me/(?P<fault_id>[0-9]+)/$', views.assign_to_me, name='assign_to_me'),
    url(r'^json/assign_to_me/(?P<fault_id>[0-9]+)/$', views_json.assign_to_me, name='assign_to_me_json'),

    # changing password
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^json/change_password/$', views_json.change_password, name='change_password_json'),
]
