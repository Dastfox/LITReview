
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import redirect, get_object_or_404

from .forms import AddFollowedUserForm
from .models import UserFollows
from .forms import ProfileForm

from django.shortcuts import render, redirect


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

    followed_by_user_ids = UserFollows.objects.filter(
        followed_user=request.user).values_list('user__id', flat=True)
    followed_by_users = User.objects.filter(id__in=followed_by_user_ids)

    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # add the followed users to the form

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
        'followed_by_users': followed_by_users,
        'form': form,
        'selected_users': None
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def abonnements(request):
    try:
        followed_user_ids = UserFollows.objects.filter(
            user=request.user).values_list('followed_user__id', flat=True)
        followed_users = User.objects.filter(id__in=followed_user_ids)
        following_user_ids = UserFollows.objects.filter(
            followed_user=request.user).values_list('user__id', flat=True)
        following_users = User.objects.filter(id__in=following_user_ids)
    except DatabaseError:
        followed_users = []
        following_users = []

    if request.method == 'POST':
        form = AddFollowedUserForm(request.POST)
        if form.is_valid():
            followed_username = form.cleaned_data['followed_users']
            try:
                followed_user = User.objects.get(username=followed_username)
                if UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                    messages.warning(
                        request, 'Vous suivez déjà cet utilisateur')
                else:
                    UserFollows.objects.create(
                        user=request.user, followed_user=followed_user)
                    messages.success(
                        request, f'Vous suivez maintenant {followed_username}')
            except User.DoesNotExist:
                messages.error(
                    request, f"L'utilisateur {followed_username} n'existe pas")
    else:
        form = AddFollowedUserForm()

    context = {'followed_users': followed_users,
               'following_users': following_users, 'form': form}
    return render(request, 'accounts/abonnements.html', context)


@login_required
def remove_followed_user(request, user_id, redirect_to='dashboard'):

    followed_user = get_object_or_404(User, id=user_id)
    print(followed_user.username, request.user.username)
    user_follows = UserFollows.objects.filter(
        user=request.user, followed_user=followed_user)
    if user_follows.exists():
        user_follows.delete()
        messages.success(
            request, f"{followed_user.username} has been removed from your followed users.")
    else:
        messages.warning(
            request, f"{followed_user.username} is not in your list of followed users.")
    return redirect(redirect_to)


@login_required
def add_followed_user(request, user_id, redirect_to='dashboard'):

    followed_user = get_object_or_404(User, id=user_id)
    print(followed_user.username, request.user.username)
    user_follows, created = UserFollows.objects.get_or_create(
        user=request.user, followed_user=followed_user)
    if created:
        messages.success(
            request, f"{followed_user.username} has been added to your followed users.")
    else:
        messages.warning(
            request, f"{followed_user.username} is already in your list of followed users.")
    return redirect(redirect_to)
