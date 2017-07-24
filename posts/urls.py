from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^list/$', views.post_list, name="list"),
	url(r'^detail/(?P<post_id>\d+)/$', views.post_detail, name="detail"),
	url(r'^create/$', views.post_create, name="create"),

]