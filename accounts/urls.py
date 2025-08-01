from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    user_login, register,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('register/', register, name='register'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
