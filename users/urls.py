from django.urls import path
from . import views


urlpatterns = [
    path("", views.profile, name="profile"),
    path("<username>/", views.profile,name="user-profile"),
    path("edit", views.profile_edit, name="profile-edit"),
    path("delete", views.profile_delete, name="profile-delete"),
    path("onboarding", views.profile_edit, name="profile-onboarding"),
    
]