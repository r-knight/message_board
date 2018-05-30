from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'submit_game', views.submit_game),
	url(r'list', views.list),
	url(r'like/(?P<game_id>\d+)', views.like_game),
	url(r'(?P<game_id>\d+)', views.view_game),
	url(r'^', views.catch_and_redirect),
]
