from itertools import chain
from django.shortcuts import get_object_or_404, redirect, render
from .models import Review, Ticket, TicketForm, ReviewForm
from django.db.models import F, Count
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
    if id:
        review = get_object_or_404(Review, pk=id, user=request.user)
        ticket = review.ticket
        ticket_form = TicketForm(request.POST or None,
                                 request.FILES or None, instance=ticket)
        review_form = ReviewForm(request.POST or None, instance=review)
    elif ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)
        ticket_form = TicketForm(request.POST or None,
                                 request.FILES or None, instance=ticket)
        review_form = ReviewForm(request.POST or None)
    else:
        ticket_form = TicketForm(request.POST or None, request.FILES or None)
        review_form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('dashboard')
    return render(request, 'dashboard/create_review.html', {'ticket_form': ticket_form, 'review_form': review_form})


def dashboard(request):
    tickets = Ticket.objects.all().annotate(review_count=Count('review'))
    # reviews = Review.objects.all()
    feed_items = sorted(
        chain(tickets),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {'feed_items': feed_items, 'show_reviews': True}
    return render(request, 'dashboard/dashboard.html', context)
