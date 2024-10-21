from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers import (
    AstronomyShowListSerializer,
    AstronomyShowRetrieveSerializer
)

ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")


def sample_astronomy_show(**params) -> AstronomyShow:
    defaults = {
        "title": "test",
        "description": "testtesttest"
    }
    defaults.update(params)
    return AstronomyShow.objects.create(**defaults)


def detail_url(astronomy_show_id: int):
    return reverse("planetarium:astronomyshow-detail", args=(astronomy_show_id,))


class UnauthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_astronomy_show_user(self):
        sample_astronomy_show()
        astronomy_show_with_show_theme = sample_astronomy_show()

        show_theme_1 = ShowTheme.objects.create(name="Space")
        show_theme_2 = ShowTheme.objects.create(name="Earth")

        astronomy_show_with_show_theme.show_theme.add(show_theme_1, show_theme_2)

        response = self.client.get(ASTRONOMY_SHOW_URL)
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_astronomy_show_by_show_themes(self):
        astronomy_show_without_show_theme = sample_astronomy_show()
        astronomy_show_with_show_theme_1 = sample_astronomy_show(title="test1")
        astronomy_show_with_show_theme_2 = sample_astronomy_show(title="test2")

        show_theme_1 = ShowTheme.objects.create(name="Space")
        show_theme_2 = ShowTheme.objects.create(name="Earth")

        astronomy_show_with_show_theme_1.show_theme.add(show_theme_1)
        astronomy_show_with_show_theme_2.show_theme.add(show_theme_2)

        response = self.client.get(ASTRONOMY_SHOW_URL, {"show_theme": f"{show_theme_1.name},{show_theme_2.name}"})

        serializer_with_show_theme_1 = AstronomyShowListSerializer(astronomy_show_with_show_theme_1)
        serializer_with_show_theme_2 = AstronomyShowListSerializer(astronomy_show_with_show_theme_2)
        serializer_without_show_theme = AstronomyShowListSerializer(astronomy_show_without_show_theme)

        response_data = list(response.data["results"])

        self.assertIn(serializer_with_show_theme_1.data, response_data)
        self.assertIn(serializer_with_show_theme_2.data, response_data)
        self.assertNotIn(serializer_without_show_theme.data, response_data)

    def test_retrieve_astronomy_show_detail(self):
        astronomy_show = sample_astronomy_show()
        astronomy_show.show_theme.add(ShowTheme.objects.create(name="Space"))

        url = detail_url(astronomy_show.id)

        response = self.client.get(url)

        serializer = AstronomyShowRetrieveSerializer(astronomy_show)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_astronomy_show_forbidden(self):
        payload = {
            "title": "test",
            "description": "testtesttest"
        }

        response = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test",
            password="adminpassword",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_astronomy_show(self):
        payload = {
            "title": "test",
            "description": "testtesttest"
        }

        response = self.client.post(ASTRONOMY_SHOW_URL, payload)

        astronomy_show = AstronomyShow.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(astronomy_show, key))

    def test_create_astronomy_show_with_show_themes(self):
        show_theme_1 = ShowTheme.objects.create(name="Space")
        show_theme_2 = ShowTheme.objects.create(name="Earth")

        payload = {
            "title": "test",
            "description": "testtesttest",
            "show_theme": [show_theme_1.id, show_theme_2.id]
        }

        response = self.client.post(ASTRONOMY_SHOW_URL, payload)

        astronomy_show = AstronomyShow.objects.get(id=response.data["id"])
        show_themes = astronomy_show.show_theme.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(show_theme_1, show_themes)
        self.assertIn(show_theme_2, show_themes)
        self.assertEqual(show_themes.count(), 2)

