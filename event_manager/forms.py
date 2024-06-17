from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser, Event


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "age",
            "bio",
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age:
            if age < 18:
                raise ValidationError("You must be 18 years or older.")
            return age
        else:
            raise ValidationError("Age is required.")


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "bio",
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age:
            if age < 18:
                raise ValidationError("You must be 18 years or older.")
            return age
        else:
            raise ValidationError("Age is required.")


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
        )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "date",
            "location",
        )
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        if date <= timezone.now():
            raise ValidationError("Date must be in the future.")
        return cleaned_data
