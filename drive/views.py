import os
from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from googleauth.models import GoogleDriveToken
from django.utils.timezone import now, timedelta
import requests

# Define media upload and download directories
UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "uploads")
DOWNLOAD_DIR = os.path.join(settings.MEDIA_ROOT, "downloads")

# Ensure media directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

from google.oauth2.credentials import Credentials

def get_drive_service(user):
    """Get Google Drive API service for the authenticated user."""
    token = GoogleDriveToken.objects.filter(user=user).first()
    if not token:
        return None

    credentials = Credentials(
        token=token.access_token,
        refresh_token=token.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
    )

    # Refresh the token if it's expired
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(requests.Request())
        # Update the database with the new access token
        token.access_token = credentials.token
        token.expires_in = now() + timedelta(seconds=3600)  # Assuming 1 hour expiry
        token.save()

    return build('drive', 'v3', credentials=credentials)


class GoogleDriveUploadView(APIView):
    """Uploads a file to the user's Google Drive"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided"}, status=400)

        drive_service = get_drive_service(request.user)
        if not drive_service:
            return Response({"error": "Google Drive not linked"}, status=400)

        # Save the file to the local 'uploads' directory
        file_path = os.path.join(UPLOAD_DIR, file.name)
        with open(file_path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Upload the file to Google Drive
        file_metadata = {"name": file.name}
        media = MediaFileUpload(file_path, resumable=True)
        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

        # Remove the file after uploading
        os.remove(file_path)

        return Response({"file_id": uploaded_file.get("id"), "message": "File uploaded successfully"})

class GoogleDriveListView(APIView):
    """Fetches all files from the user's Google Drive"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        drive_service = get_drive_service(request.user)
        if not drive_service:
            return Response({"error": "Google Drive not linked"}, status=400)

        results = drive_service.files().list(fields="files(id, name)").execute()
        files = results.get('files', [])

        return Response({"files": files})

class GoogleDriveDownloadView(APIView):
    """Downloads a file from Google Drive to local storage and returns the media URL"""
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        drive_service = get_drive_service(request.user)
        if not drive_service:
            return Response({"error": "Google Drive not linked"}, status=400)

        file = drive_service.files().get(fileId=file_id).execute()
        file_name = file["name"]
        file_path = os.path.join(DOWNLOAD_DIR, file_name)

        request = drive_service.files().get_media(fileId=file_id)
        with open(file_path, "wb") as f:
            f.write(request.execute())

        file_url = self.request.build_absolute_uri(settings.MEDIA_URL + f"downloads/{file_name}")
        return Response({"message": "File downloaded successfully", "file_url": file_url})
