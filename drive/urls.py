from django.urls import path
from .views import (
    GoogleDriveUploadView,
    GoogleDriveListView,
    GoogleDriveDownloadView
)

urlpatterns = [
    path("upload/", GoogleDriveUploadView.as_view(), name="google_drive_upload"),
    path("files/", GoogleDriveListView.as_view(), name="google_drive_files"),
    path("download/<str:file_id>/", GoogleDriveDownloadView.as_view(), name="google_drive_download"),
]
