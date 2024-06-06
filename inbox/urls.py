from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox,name="inbox"),
    path("c/<conversation_id>/", views.inbox,name="inbox"),
    path("search_users/", views.search_users,name="inbox-searchusers"),
    path("new-message/<recipient_id>", views.new_message,name="inbox-newmessage"),
]