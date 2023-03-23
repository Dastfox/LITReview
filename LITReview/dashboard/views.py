from itertools import chain
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import UserFollows
from .models import Review, Ticket, TicketForm, ReviewForm
from django.db.models import F, Count
from django.contrib.auth.models import User
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


def dashboard(request, feed_type='dashboard'):
    followed_user_ids = UserFollows.objects.filter(
        user=request.user).values_list('followed_user__id', flat=True)
    followed_users = User.objects.filter(id__in=followed_user_ids)

    if feed_type == 'posts':
        tickets = Ticket.objects.filter(user=request.user).annotate(
            review_count=Count('review'))
    elif feed_type == 'abonnements':
        tickets = Ticket.objects.filter(user__in=followed_users).annotate(
            review_count=Count('review'))
    else:
        tickets = Ticket.objects.all().annotate(review_count=Count('review'))

    feed_items = sorted(
        chain(tickets),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {'feed_items': feed_items,
               'show_reviews': True, 'feed_type': feed_type, 'followed_users': followed_users}
    return render(request, 'dashboard/dashboard.html', context)
