from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    agree_terms = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'برای ثبت‌ نام باید با شرایط استفاده موافقت کنید.'
        }
    )
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "agree_terms")
        
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("ایمیل قبلا ثبت شده است")

        return email
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                pass

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError("نام کاربری یا ایمیل شما اشتباه است")

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['email'].widget.attrs.update({
            'class':'form-control border-0 bg-light rounded-end ps-1',
            'placeholder':'example@gmail.com'
        })

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': '*********'
        })

        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control border-0 bg-light rounded-end ps-1',
            'placeholder': '*********'
        })