from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


from .forms import *
from .models import *


class HomePageView(TemplateView):
    template_name = "homePage.html"

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        date = request.GET.get("date")

        events = Event.objects.all().filter(date__gte=timezone.now()).order_by("date")
        if date:
            events = events.filter(date__date=date)
        if query:
            events = events.filter(Q(title__icontains=query) | Q(organizer__username__icontains=query))
        return render(request, self.template_name, {"events": events})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)


class LogInView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_new.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        registrations = Registration.objects.select_related('attendee').filter(event=event)
        attendees = [registration.attendee for registration in registrations]
        return render(request, self.template_name, {"event": event, "attendees": attendees})


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event_edit.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user != event.organizer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Event updated successfully.")
            return redirect("event_detail", event.pk)
        return render(request, self.template_name, {"form": form})


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = "event_delete.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user != event.organizer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect("home")


class EventJoinView(LoginRequiredMixin, CreateView):

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        if event.organizer == request.user:
            messages.error(request, "You cannot join your own event.")
            return redirect("event_detail", event.pk)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        registration = Registration.objects.create(attendee=request.user, event=event)
        registration.save()
        messages.success(request, "Event joined successfully.")
        return redirect("event_detail", event.pk)


class EventLeaveView(LoginRequiredMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        registration = Registration.objects.get(attendee=request.user, event=event)
        if registration is None:
            messages.error(request, "You are not registered for this event.")
            return redirect("event_detail", event.pk)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        registration = Registration.objects.get(attendee=request.user, event=event)
        registration.delete()
        messages.success(request, "Event left successfully.")
        return redirect("event_detail", event.pk)


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        if request.user != user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        return render(request, self.template_name, {"user": user})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def dispatch(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        if request.user != user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user.age = form.cleaned_data["age"]
            user.bio = form.cleaned_data["bio"]
            user = form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile", user.pk)
        return render(request, self.template_name, {"form": form})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "profile_delete.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        if request.user != user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        user.delete()
        messages.success(request, "Profile deleted successfully.")
        return redirect("home")


class AttendingListView(LoginRequiredMixin, ListView):
    template_name = "attending.html"

    def dispatch(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        if request.user != user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        registrations = Registration.objects.all().filter(attendee=user).order_by("event__date")
        future_events = [registration.event for registration in registrations.filter(event__date__gte=timezone.now())]
        past_events = [registration.event for registration in registrations.filter(event__date__lt=timezone.now())]
        return render(request, self.template_name, {"past_events": past_events, "future_events": future_events})


class HostingListView(LoginRequiredMixin, ListView):
    template_name = "hosting.html"

    def dispatch(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        if request.user != user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        future_events = Event.objects.all().filter(organizer=user).filter(date__gte=timezone.now()).order_by("date")
        past_events = Event.objects.all().filter(organizer=user).filter(date__lt=timezone.now()).order_by("date")
        return render(request, self.template_name, {"past_events": past_events, "future_events": future_events})


class ParticipantsListView(LoginRequiredMixin, ListView):
    template_name = "participants.html"

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        if request.user != event.organizer:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs["pk"])
        registrations = Registration.objects.select_related('attendee').filter(event=event)
        participants = [registration.attendee for registration in registrations]
        num_participants = len(participants)
        return render(request, self.template_name, {"event": event, "participants": participants,
                                                    "num_participants": num_participants})


class OrganizerView(TemplateView):
    model = CustomUser
    template_name = "organizer.html"

    def get(self, request, *args, **kwargs):
        organizer = Event.objects.get(pk=kwargs["pk"]).organizer
        events = Event.objects.all().filter(organizer=organizer).filter(date__gte=timezone.now()).order_by("date")
        return render(request, self.template_name, {"organizer": organizer, "events": events})
