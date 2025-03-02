from django.db import models
from django.contrib.auth.models import User
from django.db import models

class GoogleDriveToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_in = models.DateTimeField()
