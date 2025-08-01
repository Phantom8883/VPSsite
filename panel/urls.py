from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('', views.home, name='home'),                # Главная страница (доступна всем)
    path('dashboard/', views.dashboard, name='dashboard'),  # Личный кабинет (только для авторизованных)
    path('profile/', views.profile, name='profile'),        # Профиль (только для авторизованных)
]
