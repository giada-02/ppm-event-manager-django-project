from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/<int:pk>/delete/", ProfileDeleteView.as_view(), name="profile_delete"),
    path("event/new/", EventCreateView.as_view(), name="event_new"),
    path("event/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("event/<int:pk>/edit/", EventUpdateView.as_view(), name="event_edit"),
    path("event/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
    path("event/<int:pk>/join/", EventJoinView.as_view(), name="event_join"),
    path("event/<int:pk>/leave/", EventLeaveView.as_view(), name="event_leave"),
    path("event/<int:pk>/hosting/", HostingListView.as_view(), name="hosting"),
    path("event/<int:pk>/attending/", AttendingListView.as_view(), name="attending"),
    path("event/<int:pk>/participants/", ParticipantsListView.as_view(), name="participants"),
    path("organizer/<int:pk>/", OrganizerView.as_view(), name="organizer"),
]
