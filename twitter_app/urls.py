from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^twitter/$', views.twitterAPI, name="twitter"),
]