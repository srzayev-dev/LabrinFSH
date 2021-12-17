from django.urls import path
from . import views

# app_name = "fileapp"

urlpatterns = [
    path("", views.home_view, name = "home"),
    path("fileList/", views.FileListView.as_view(), name="listFile"),
    path("detail/<int:pk>/", views.FileDetailView.as_view(), name="detailFile"),
    path("sharedFile/", views.sharedFileListView.as_view(), name="sharedFile"),
    path("openFile/<int:pk>/", views.OpenFileView.as_view(), name="openFile"),
]
