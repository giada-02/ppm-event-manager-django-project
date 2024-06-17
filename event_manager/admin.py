from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "age",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),)


admin.site.register(CustomUser, CustomUserAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "date",
        "location",
        "organizer",
    ]


class RegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "event",
        "attendee",
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(Registration, RegistrationAdmin)
