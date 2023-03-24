from django.db.models import Q
from .models import Ticket
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from itertools import chain
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import UserFollows
from .models import Review, Ticket
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import TicketForm, ReviewForm
# Create your views here.


# def dashboard(request):
#     return render(request, 'dashboard/dashboard.html')


def create_ticket(request, id=None):
    if id:
        ticket = get_object_or_404(Ticket, pk=id, user=request.user)
        form = TicketForm(request.POST or None,
                          request.FILES or None, instance=ticket)
    else:
        form = TicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('dashboard')
    return render(request, 'dashboard/create_ticket.html', {'form': form})


def delete_ticket(request, id, redirect_to='dashboard'):
    ticket = get_object_or_404(Ticket, pk=id, user=request.user)
    ticket.delete()
    return redirect(redirect_to)


def create_review(request, ticket_id=None, id=None):
    ticket = None
    print(ticket_id, id)
    if id:
        review = get_object_or_404(Review, pk=id, user=request.user)
        ticket = review.ticket
        ticket_form = TicketForm(request.POST or None,
                                 request.FILES or None, instance=ticket)
        review_form = ReviewForm(request.POST or None, instance=review)
    elif ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        print(ticket)
        ticket_form = TicketForm(request.POST or None,
                                 request.FILES or None, instance=ticket)
        review_form = ReviewForm(request.POST or None)
    else:
        ticket_form = TicketForm(request.POST or None, request.FILES or None)
        review_form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()

            review.save()
            return redirect('dashboard')
    return render(request, 'dashboard/create_review.html', {'ticket_form': ticket_form, 'review_form': review_form, 'ticket': ticket})


def delete_review(request, id, redirect_to='dashboard'):
    review = get_object_or_404(Review, pk=id, user=request.user)
    review.delete()
    return redirect(redirect_to)


def dashboard(request, feed_type=None):
    followed_user_ids = UserFollows.objects.filter(
        user=request.user).values_list('followed_user__id', flat=True)
    followed_users = User.objects.filter(id__in=followed_user_ids)
    user_tickets = Ticket.objects.filter(
        user=request.user).annotate(review_count=Count('review'))
    other_tickets = Ticket.objects.filter(user__in=followed_users).exclude(
        user=request.user).annotate(review_count=Count('review'))
    remaining_tickets = Ticket.objects.exclude(Q(user__in=followed_users) | Q(
        user=request.user)).annotate(review_count=Count('review'))
    sorted_tickets = sorted(chain(user_tickets, other_tickets, remaining_tickets),
                            key=lambda instance: instance.time_created, reverse=True)
    context = {
        'feed_items': sorted_tickets,
        'show_reviews': True,
        'feed_type': 'dashboard',
        'followed_users': followed_users,
        'rating_range': range(1, 6),
    }
    return render(request, 'dashboard/dashboard.html', context)


def posts(request, feed_type=None):
    followed_user_ids = UserFollows.objects.filter(
        user=request.user).values_list('followed_user__id', flat=True)
    followed_users = User.objects.filter(id__in=followed_user_ids)

    # Fetch tickets created by the user
    user_tickets = Ticket.objects.filter(
        user=request.user).annotate(review_count=Count('review'))

    # Fetch tickets with reviews written by the user
    user_reviewed_tickets = Ticket.objects.filter(
        review__user=request.user).annotate(review_count=Count('review'))

    # Combine user_tickets and user_reviewed_tickets, removing duplicates using the "distinct" method
    combined_tickets = user_tickets | user_reviewed_tickets
    combined_tickets = combined_tickets.distinct().order_by('-time_created')

    context = {
        'feed_items': combined_tickets,
        'show_reviews': True,
        'feed_type': 'dashboard',
        'followed_users': followed_users,
        'page_title': 'posts',
        'rating_range': range(1, 6),
    }
    return render(request, 'dashboard/dashboard.html', context)
