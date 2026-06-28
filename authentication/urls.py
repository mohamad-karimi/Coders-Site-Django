from django.urls import path,reverse_lazy
from authentication.views import sign_in, sign_up, logout_view
from django.contrib.auth import views as auth_views
from authentication.form import CustomPasswordResetForm, CustomSetPasswordForm

app_name="authentication"

urlpatterns = [
    path('login/', sign_in, name='login'),
    path('Logout', logout_view, name='logout'),
    path('signup/', sign_up, name='signup'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name='authentication/password_reset.html',
        email_template_name='authentication/password_reset_email.html',
        success_url=reverse_lazy('authentication:password_reset_done'),
    ), name='password_reset'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=CustomSetPasswordForm,
        template_name='authentication/password_reset_confirm.html',
        success_url=reverse_lazy('authentication:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='authentication/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='authentication/password_reset_complete.html'
    ), name='password_reset_complete'),
]