from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('abonnements/', login_required(lambda request: views.dashboard(request, feed_type='abonnements')),
         name='abonnements'),
    path('posts/', login_required(lambda request: views.dashboard(request,
                                                                  feed_type='posts')), name='posts'),
    path('new-ticket/', login_required(views.create_ticket), name='new-ticket'),
    path('new-review/', login_required(views.create_review), name='new-review'),
    path('new-review/<int:ticket_id>/',
         login_required(views.create_review), name='new-review-with-ticket'),

    path('update-ticket/<int:id>/',
         login_required(views.create_ticket), name='update-ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
