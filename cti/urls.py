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
    url(r'^json/searched_faults/$', views_json.searched_faults, name='searched_faults_json'),

    # adding fault
    url(r'^add_fault/$', views.add_fault, name='add_fault'),
    url(r'^json/add_fault$', views_json.add_fault, name='add_fault_json'),

    # editing fault
    url(r'^edit_fault/(?P<fault_id>[0-9]+)/$', views.edit_fault, name='edit_fault'),
    url(r'^json/edit_fault/(?P<fault_id>[0-9]+)/$', views_json.edit_fault, name='edit_fault_json'),

    # details of fault
    url(r'^fault_details/(?P<fault_id>[0-9]+)/$', views.fault_details, name='fault_details'),
    url(r'^json/fault_details/(?P<fault_id>[0-9]+)/$', views_json.fault_details, name='fault_details_json'),

    # details of object
    url(r'^object_details/(?P<object_id>[0-9]+)/$', views.object_details, name='object_details'),
    url(r'^json/object_details/(?P<object_id>[0-9]+)/$', views_json.object_details, name='object_details_json'),

    # details of user
    url(r'^user_details/$', views.user_details, name='user_details'),
    url(r'^json/user_details/$', views_json.user_details, name='user_details_json'),

    # admin - index
    url(r'^admin/index/$', views_admin.index, name='index_admin'),

    # admin - my faults
    url(r'^admin/my_faults/$', views_admin.my_faults, name='my_faults_admin'),

    # admin - resolved faults
    url(r'^admin/resolved_faults/$', views_admin.resolved_faults, name='resolved_faults_admin'),

    # admin - deleted faults
    url(r'^admin/deleted_faults/$', views_admin.deleted_faults, name='deleted_faults_admin'),

    # admin - details of fault
    url(r'^admin/fault_details/(?P<fault_id>[0-9]+)/$', views_admin.fault_details, name='fault_details_admin'),

    # admin - details of object
    url(r'^admin/object_details/(?P<object_id>[0-9]+)/$', views_admin.object_details, name='object_details_admin'),

    # admin - details of user
    url(r'^admin/user_details/$', views_admin.user_details, name='user_details_admin'),

    # admin - editing fault
    url(r'^admin/edit_fault/(?P<fault_id>[0-9]+)/$', views_admin.edit_fault, name='edit_fault_admin'),

    # admin - assigning fault
    url(r'^admin/assign_to_me/(?P<fault_id>[0-9]+)/$', views_admin.assign_to_me, name='assign_to_me_admin'),

    # admin - reassigning fault
    url(r'^admin/fault_details/(?P<fault_id>[0-9]+)/reassign_fault/(?P<username>[0-9]+)$', views_admin.reassign_fault, name='reassign_fault_admin'),

    # admin - deleting fault
    url(r'^admin/delete_fault/(?P<fault_id>[0-9]+)/$', views_admin.delete_fault, name='delete_fault_admin'),

    # admin - all users
    url(r'^admin/users/$', views_admin.all_users, name='all_users_admin'),

    # admin - change password
    url(r'^admin/change_password/$', views_admin.change_password, name='change_password_admin'),

    # admin - ask for reassign
    url(r'^admin/fault_details/(?P<fault_id>[0-9]+)/ask_for_reassign/(?P<username>[0-9]+)$', views_admin.ask_for_reassign, name='ask_for_reassign_admin'),

    # admin - report phone number
    url(r'^admin/fault_details/(?P<fault_id>[0-9]+)/report_phone_number/$', views_admin.report_phone_number, name='report_phone_number_admin'),
]
