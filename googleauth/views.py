# views.py
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.http import JsonResponse
import requests
from django.utils.timezone import now, timedelta
from django.contrib.auth import authenticate, login, get_user_model
from .models import GoogleDriveToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

REDIRECT_URI = "https://enfund-3bc4b732ed3d.herokuapp.com/auth/social/google/login/callback/"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
User = get_user_model()



def google_login(request):
    """
    Step 1: Redirect user to Google's OAuth login page.
    """
    print(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
    print(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET)
    params = {
        "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/drive.file",
        "redirect_uri": REDIRECT_URI,
        "prompt": "consent",
        "access_type": "offline",
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return redirect(auth_url)


def google_callback(request):
    """
    Step 2: Handle the callback from Google.
    Exchange authorization code for access token & fetch user info.
    If the user exists, log them in. Otherwise, create a new user and log them in.
    """
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    # Exchange authorization code for tokens
    token_data = {
        "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()

    if "access_token" not in token_json:
        return JsonResponse({"error": "Failed to get access token", "details": token_json}, status=400)

    access_token = token_json["access_token"]
    refresh_token = token_json.get("refresh_token")
    expires_in = now() + timedelta(seconds=token_json["expires_in"])

    # Fetch user info
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
    user_info = user_info_response.json()

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        return JsonResponse({"error": "Unable to fetch email from Google"}, status=400)

    # Check if user exists
    user = User.objects.filter(email=email).first()

    if not user:
        # If user does not exist, create a new one
        user = User.objects.create(username=email, email=email, first_name=name)
        user.set_unusable_password()  # Since authentication is via Google, disable password login
        user.save()

    # Store or update Google Drive tokens
    GoogleDriveToken.objects.update_or_create(
        user=user,
        defaults={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
        }
    )

    # Log the user in
    tokens = get_tokens_for_user(user)

    return JsonResponse({
        "message": "User authenticated successfully!",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.first_name
        },
        "tokens": tokens
    })
