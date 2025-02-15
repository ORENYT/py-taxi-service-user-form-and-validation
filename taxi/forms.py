from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(forms.ModelForm):
    LICENSE_LENGTH = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self) -> str:
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != self.LICENSE_LENGTH:
            raise ValidationError(
                f"License number must consist only {self.LICENSE_LENGTH} "
                f"numbers. {len(license_number)} provided."
            )
        if not license_number[:3].isalpha():
            raise ValidationError("First 3 characters must be letters.")
        if not license_number[:3].isupper():
            raise ValidationError("First 3 characters must be uppercase.")
        if not license_number[-5:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")
        return license_number


class CarCreateUpdateForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverCreateForm(UserCreationForm, DriverLicenseUpdateForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)
