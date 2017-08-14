from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^text/$', views.text_search, name="text"),
	url(r'^detail/$', views.place_detail, name="detail"),
	url(r'^nearby/$', views.nearby_search, name="nearby"),
]