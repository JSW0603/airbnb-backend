import jwt
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
PASSWORD = "testpass123"

USER_DATA = {
    "username": "jinwoo",
    "gender": "male",
    "language": "en",
    "currency": "eur",
}


def make_user(**kwargs):
    data = {**USER_DATA, **kwargs}
    user = User.objects.create(
        username=data["username"],
        gender=data["gender"],
        language=data["language"],
        currency=data["currency"],
    )
    user.set_password(PASSWORD)
    user.save()
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return make_user()


@pytest.mark.django_db
def test_jwt_login_returns_decodable_token(client, user):
    res = client.post(
        "/api/v1/users/jwt-login",
        {"username": "jinwoo", "password": PASSWORD},
    )
    assert res.status_code == 200
    token = res.data["token"]
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert decoded["pk"] == user.pk


@pytest.mark.django_db
def test_jwt_login_wrong_password(client, user):
    res = client.post(
        "/api/v1/users/jwt-login",
        {"username": "jinwoo", "password": "wrongpass"},
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_jwt_login_missing_password(client, user):
    res = client.post("/api/v1/users/jwt-login", {"username": "jinwoo"})
    assert res.status_code == 400