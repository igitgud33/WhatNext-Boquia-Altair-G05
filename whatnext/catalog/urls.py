from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.media_list, name="media_list"),
    path("add/", views.add_media, name="add_media"),
    path("add-to-backlog/<int:media_id>/", views.add_to_backlog, name="add_to_backlog"),
    path("my-backlog/", views.my_backlog, name="my_backlog"),
    path("update-status/<int:entry_id>/", views.update_backlog_status, name="update_backlog_status"),
    path("remove-from-backlog/<int:entry_id>/", views.remove_from_backlog, name="remove_from_backlog"),
    path("edit/<int:media_id>/", views.edit_media, name="edit_media"),
]