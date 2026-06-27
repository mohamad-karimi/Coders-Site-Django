# forms.py
from django import forms
from django.contrib.auth import get_user_model
from authentication.models import CustomUser
User = get_user_model()

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "first_name", "last_name", "username"]

class EmailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً استفاده شده است")

        return email
    
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]

        if not self.user.check_password(old_password):
            raise forms.ValidationError("رمز فعلی اشتباه است")

        return old_password

def clean(self):
    cleaned_data = super().clean()

    old_password = cleaned_data.get("old_password")
    new_password = cleaned_data.get("new_password")
    confirm_password = cleaned_data.get("confirm_password")

    if new_password and confirm_password:
        if new_password != confirm_password:
            raise forms.ValidationError("رمز جدید و تایید آن یکسان نیست")

        if old_password == new_password:
            raise forms.ValidationError("رمز جدید نمی‌تواند مثل رمز قبلی باشد")

    return cleaned_data