import datetime

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from categories.models import Category
from experiences.models import Content, Experience

User = get_user_model()
PASSWORD = "secret123"

EXPERIENCE_DATA = {
    "name": "Tapas tour",
    "country": "Spain",
    "city": "Granada",
    "price": 50,
    "address": "Plaza Nueva 1",
    "starts_at": "10:00:00",
    "end": "12:00:00",
    "description": "A walking tapas tour.",
}


def make_user(username="jinwoo", **kwargs):
    user = User.objects.create(
        username=username,
        gender="male",
        language="en",
        currency="eur",
        **kwargs,
    )
    user.set_password(PASSWORD)
    user.save()
    return user


def make_experience(host, category=None, **kwargs):
    data = {
        "country": "Spain",
        "city": "Granada",
        "name": "Tapas tour",
        "host": host,
        "price": 50,
        "address": "Plaza Nueva 1",
        "starts_at": datetime.time(10, 0),
        "end": datetime.time(12, 0),
        "description": "A walking tapas tour.",
        "category": category,
    }
    data.update(kwargs)
    return Experience.objects.create(**data)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def host():
    return make_user()


@pytest.fixture
def other_user():
    return make_user(username="guest")


@pytest.fixture
def category():
    return Category.objects.create(
        name="Cooking", kind=Category.CategoryKindChoices.EXPERIENCES
    )


@pytest.fixture
def content():
    return Content.objects.create(name="Ingredients included")


@pytest.mark.django_db
def test_list_empty(client):
    res = client.get("/api/v1/experiences/")
    assert res.status_code == 200
    assert res.data == []


@pytest.mark.django_db
def test_list_shows_is_host_for_host(client, host, category):
    make_experience(host=host, category=category)
    client.force_authenticate(user=host)
    res = client.get("/api/v1/experiences/")
    assert res.status_code == 200
    assert res.data[0]["is_host"] is True


@pytest.mark.django_db
def test_create_experience(client, host, category, content):
    client.force_authenticate(user=host)
    res = client.post(
        "/api/v1/experiences/",
        {**EXPERIENCE_DATA, "category": category.pk, "contents": [content.pk]},
        format="json",
    )
    assert res.status_code == 200
    assert Experience.objects.filter(name="Tapas tour").exists()


@pytest.mark.django_db
def test_create_requires_category(client, host, content):
    client.force_authenticate(user=host)
    res = client.post(
        "/api/v1/experiences/",
        {**EXPERIENCE_DATA, "contents": [content.pk]},
        format="json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_detail_for_host_shows_is_host_true(client, host, category):
    exp = make_experience(host=host, category=category)
    client.force_authenticate(user=host)
    res = client.get(f"/api/v1/experiences/{exp.pk}/")
    assert res.status_code == 200
    assert res.data["is_host"] is True


@pytest.mark.django_db
def test_detail_anonymous_is_host_false(client, host, category):
    exp = make_experience(host=host, category=category)
    res = client.get(f"/api/v1/experiences/{exp.pk}/")
    assert res.status_code == 200
    assert res.data["is_host"] is False


@pytest.mark.django_db
def test_detail_404(client):
    assert client.get("/api/v1/experiences/9999/").status_code == 404


@pytest.mark.django_db
def test_host_can_update(client, host, category, content):
    exp = make_experience(host=host, category=category)
    client.force_authenticate(user=host)
    res = client.put(
        f"/api/v1/experiences/{exp.pk}/",
        {
            "name": "Flamenco night",
            "category": category.pk,
            "contents": [content.pk],
        },
        format="json",
    )
    assert res.status_code == 200
    exp.refresh_from_db()
    assert exp.name == "Flamenco night"


@pytest.mark.django_db
def test_non_host_update_forbidden(client, host, other_user, category, content):
    exp = make_experience(host=host, category=category)
    client.force_authenticate(user=other_user)
    res = client.put(
        f"/api/v1/experiences/{exp.pk}/",
        {
            "name": "Flamenco night",
            "category": category.pk,
            "contents": [content.pk],
        },
        format="json",
    )
    assert res.status_code == 403


@pytest.mark.django_db
def test_host_can_delete(client, host, category):
    exp = make_experience(host=host, category=category)
    client.force_authenticate(user=host)
    res = client.delete(f"/api/v1/experiences/{exp.pk}/")
    assert res.status_code == 204
    assert not Experience.objects.filter(pk=exp.pk).exists()


@pytest.mark.django_db
def test_non_host_delete_forbidden(client, host, other_user, category):
    exp = make_experience(host=host, category=category)
    client.force_authenticate(user=other_user)
    res = client.delete(f"/api/v1/experiences/{exp.pk}/")
    assert res.status_code == 403


@pytest.mark.django_db
def test_content_delete(client, content):
    res = client.delete(f"/api/v1/experiences/Contents/{content.pk}/")
    assert res.status_code == 204
    assert not Content.objects.filter(pk=content.pk).exists()