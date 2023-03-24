from django.conf import settings
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db import transaction


from django import forms
from django.contrib.auth.models import User
from django.db import transaction


# Create your models here.

class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    class Meta:
        unique_together = ('user', 'followed_user',)

# binding between user and followed user


