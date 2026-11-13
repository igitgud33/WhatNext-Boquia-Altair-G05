from django.urls import path
from .views import DashboardView, AdminPaneView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin-panel/", AdminPaneView.as_view(), name="admin_panel"),
]