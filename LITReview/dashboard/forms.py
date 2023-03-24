from django import forms
from .models import Ticket, Review




class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['t_title', 't_description', 'image']



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
