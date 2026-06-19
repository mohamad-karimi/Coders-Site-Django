from django.urls import path
from authentication.views import sign_in, sign_up, forgot_password

urlpatterns = [
    path('login/', sign_in, name='login'),
    path('signup/', sign_up, name='signup'),
    path('password-reset/', forgot_password, name='password_reset'),
]