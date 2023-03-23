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


class ProfileForm(forms.ModelForm):
    followed_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'followed-users'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        followed_users = kwargs.pop('followed_users', None)
        super().__init__(*args, **kwargs)
        self.fields['followed_users'].initial = followed_users or User.objects.none()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            with transaction.atomic():
                # Add new followed users
                followed_users = self.cleaned_data['followed_users']
                if followed_users:
                    for user in followed_users:
                        UserFollows.objects.create(
                            user=instance, followed_user=user)
        return instance
