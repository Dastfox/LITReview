
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import transaction

from .models import UserFollows
from .models import ProfileForm

from django.shortcuts import render, redirect

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Votre compte a été créé, vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    # Retrieve list of followed users for the current user
    followed_user_ids = UserFollows.objects.filter(
        user=request.user).values_list('followed_user__id', flat=True)
    followed_users = User.objects.filter(id__in=followed_user_ids)

    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Profile update failed.')
    else:
        # Create a new form instance with the current user and the list of followed users
        form = ProfileForm(instance=request.user,
                           followed_users=followed_users)

    context = {
        'users': users,
        'followed_users': followed_users,
        'form': form
    }

    return render(request, 'accounts/profile.html', context)
