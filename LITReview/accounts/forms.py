from django.conf import settings
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db import transaction


from django import forms
from django.contrib.auth.models import User
from django.db import transaction

from .models import UserFollows



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
        print("TRUC", self.cleaned_data['followed_users'])
        instance = super().save(commit=commit)
        if commit:
            with transaction.atomic():
                # Delete existing followed users
                UserFollows.objects.filter(followed_user=instance).delete()

                # Add new followed users
                followed_users = self.cleaned_data['followed_users']
                if followed_users:
                    for user in followed_users:
                        UserFollows.objects.create(
                            user=instance, followed_user=user)
        return instance


class AddFollowedUserForm(forms.Form):
    followed_users = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
