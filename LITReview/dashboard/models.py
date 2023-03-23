from django import forms
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Ticket(models.Model):
    t_title = models.CharField(max_length=128)
    t_description = models.TextField(max_length=2048)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['t_title', 't_description', 'image']


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    r_title = models.CharField(max_length=128)
    r_description = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class MergedReviewTicketForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ticket', 'rating', 'r_title', 'r_description']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5}),
            'r_title': forms.TextInput(attrs={'maxlength': 128}),
            'r_description': forms.Textarea(attrs={'maxlength': 8192}),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    rating = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        choices=RATING_CHOICES,
        error_messages={'required': 'Please select a rating.'},
    )

    class Meta:
        model = Review
        fields = ['ticket', 'rating', 'r_title', 'r_description']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5}),
            'r_title': forms.TextInput(attrs={'maxlength': 128}),
            'r_description': forms.Textarea(attrs={'maxlength': 8192}),
        }
