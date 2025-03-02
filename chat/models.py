from django.db import models


# Create your models here.

class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField('user.User', related_name='chat_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
