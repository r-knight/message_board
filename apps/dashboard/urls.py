from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'admin_dashboard', views.admin_dashboard),
	url(r'dashboard', views.dashboard),
	url(r'redirect', views.route_to_dashboard),
	url(r'admin/add', views.add_user),
	url(r'^', views.home),
]