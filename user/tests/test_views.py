import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_profile_view(client, django_user_model):
    # создаём фейкового пользователя
    user = django_user_model.objects.create_user(username="testuser", password="1234")
    
    # логинимся
    client.login(username="testuser", password="1234")
    
    # открываем страницу профиля
    response = client.get(reverse("profile"))  # "profile" — это имя маршрута
    assert response.status_code == 200
