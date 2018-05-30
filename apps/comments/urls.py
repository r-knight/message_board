from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'((?P<comment_id>\d+)/edit_comment)', views.edit_comment),
	url(r'((?P<comment_id>\d+)/submit_edit)', views.submit_edit),
	url(r'((?P<comment_id>\d+)/delete_comment)', views.delete_comment),
	url(r'like/(?P<comment_id>\d+)', views.like_comment),
	url(r'((?P<page_id>\d+)/submit_comment)', views.submit_comment),
	url(r'submit_comment_new', views.submit_comment_new),
]
