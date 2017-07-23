from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.post_create, name="Create"),
    url(r'^update/$', views.post_update, name="Update"),
    url(r'^delete/$', views.post_delete, name="Delete"),
    url(r'^list/$', views.post_list, name="List"),
    url(r'^detail/$', views.post_detail, name="Detail"),
    url(r'^content/$', views.post_content, name="Content"),
    url(r'^image/$', views.post_image, name="Image"),
    url(r'^contact/$', views.post_contact, name="Contact")

]