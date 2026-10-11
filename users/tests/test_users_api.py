import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
PASSWORD = "secret123"

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
def test_register_creates_user(client):
    res = client.post("/api/v1/users/", {**USER_DATA, "password": PASSWORD})
    assert res.status_code == 200
    assert User.objects.filter(username="jinwoo").exists()
    assert "password" not in res.data  # 비밀번호 해시가 응답에 노출되면 안 됨


@pytest.mark.django_db
def test_register_requires_password(client):
    res = client.post("/api/v1/users/", USER_DATA)
    assert res.status_code == 400


@pytest.mark.django_db
def test_login_then_me(client, user):
    res = client.post(
        "/api/v1/users/login", {"username": "jinwoo", "password": PASSWORD}
    )
    assert res.status_code == 200
    me = client.get("/api/v1/users/me")
    assert me.status_code == 200
    assert me.data["username"] == "jinwoo"


@pytest.mark.django_db
def test_login_wrong_password(client, user):
    res = client.post(
        "/api/v1/users/login", {"username": "jinwoo", "password": "wrongpass"}
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_me_requires_auth(client):
    assert client.get("/api/v1/users/me").status_code == 403


@pytest.mark.django_db
def test_change_password(client, user):
    client.login(username="jinwoo", password=PASSWORD)
    res = client.put(
        "/api/v1/users/change-password",
        {"old_password": PASSWORD, "new_password": "newsecret456"},
        format="json",
    )
    assert res.status_code == 200
    user.refresh_from_db()
    assert user.check_password("newsecret456")


@pytest.mark.django_db
def test_change_password_wrong_old_password(client, user):
    client.login(username="jinwoo", password=PASSWORD)
    res = client.put(
        "/api/v1/users/change-password",
        {"old_password": "wrongpass", "new_password": "newsecret456"},
        format="json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_public_profile(client, user):
    res = client.get("/api/v1/users/@jinwoo")
    assert res.status_code == 200
    assert client.get("/api/v1/users/@ghost").status_code == 404