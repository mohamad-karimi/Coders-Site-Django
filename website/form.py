from django import forms
from website.models import contact


class contactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['name', 'email', 'message']