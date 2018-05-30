from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'login', views.login),
	url(r'existing', views.existing),
	url(r'logout', views.logout),
	url(r'register', views.register),
	url(r'submit_new_user', views.submit_new_user),
	url(r'new', views.new),
	url(r'success', views.success),
	url(r'index', views.index),
	url(r'flush_all', views.flush_all),
	url(r'myaccount/(?P<user_id>\d+)', views.edit),
	url(r'admin/edit/(?P<user_id>\d+)', views.admin_edit),
	url(r'admin/delete/(?P<user_id>\d+)', views.admin_delete),
	url(r'admin/delete_profile', views.admin_delete_profile),
	url(r'admin/cancel_delete', views.admin_cancel_delete),
	url(r'admin_edit_profile', views.admin_edit_profile),
	url(r'admin_edit_password', views.admin_edit_password),
	url(r'edit_profile', views.edit_profile),
	url(r'(?P<user_id>\d+)', views.view_user),
	url(r'^', views.index),
]
