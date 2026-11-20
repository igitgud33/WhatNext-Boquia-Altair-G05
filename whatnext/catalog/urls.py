from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.media_list, name="media_list"),
    path("add/", views.add_media, name="add_media")
]