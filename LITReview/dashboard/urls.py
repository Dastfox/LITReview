from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('posts/', login_required(views.posts), name='posts'),
    path('new-ticket/', login_required(views.create_ticket), name='new-ticket'),
    path('new-review/', login_required(views.create_review), name='new-review'),
    path('new-review/<int:ticket_id>/',
         login_required(views.create_review), name='new-review-with-ticket'),

    path('update-ticket/<int:id>/',
         login_required(views.create_ticket), name='update-ticket'),
    path('update-review/<int:id>/',
         login_required(views.create_review), name='update-review'),
    path('delete-ticket/<int:id>/', login_required(
         views.delete_ticket), name='delete-ticket'),
    path('delete-review/<int:id>/', login_required(
         views.delete_review), name='delete-review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
