from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Тут логин/регистрация/логаут
    path('user/', include('user.urls')),          # Тут профиль, настройки пользователя
    path('', include('panel.urls')),              # Панель — главная страница после входа
    #path('vps/', include('vps.urls')),
# billing и support — подключим после создания
]
