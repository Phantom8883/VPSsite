from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.urls import path
from . import views_dev

urlpatterns = [
    # твои настоящие пути
]

if settings.DEBUG:
    urlpatterns += [
        path("dev/test-style/", views_dev.test_style),
    ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Тут логин/регистрация/логаут
    path('user/', include('user.urls')),          # Тут профиль, настройки пользователя
    path('', include('panel.urls')),              # Панель — главная страница после входа
    #path('vps/', include('vps.urls')),
# billing и support — подключим после создания
]
