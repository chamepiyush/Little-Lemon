from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from restaurant.models import Booking, Menu
from restaurant.serializers import MenuSerializer


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Menu.objects.create(title="IceCream", price=80, inventory=100)
        Menu.objects.create(title="Pasta", price=120, inventory=50)

    def test_getall(self):
        response = self.client.get("/api/menu/")
        expected = MenuSerializer(Menu.objects.all(), many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    def test_anonymous_cannot_create_menu_item(self):
        response = self.client.post(
            "/api/menu/", {"title": "Soup", "price": "30.00", "inventory": 5}
        )
        self.assertIn(response.status_code, (401, 403))

    def test_authenticated_can_create_menu_item(self):
        user = User.objects.create_user("chef", password="pass12345!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.post(
            "/api/menu/", {"title": "Soup", "price": "30.00", "inventory": 5}
        )
        self.assertEqual(response.status_code, 201)


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("guest", password="pass12345!")
        self.token = Token.objects.create(user=self.user)

    def test_booking_requires_auth(self):
        self.assertIn(self.client.get("/api/tables/").status_code, (401, 403))

    def test_booking_crud(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        payload = {"name": "Anna", "no_of_guests": 3, "booking_date": "2026-12-01T19:00:00Z"}
        created = self.client.post("/api/tables/", payload, format="json")
        self.assertEqual(created.status_code, 201)
        pk = created.data["id"]

        self.assertEqual(self.client.get("/api/tables/").status_code, 200)

        payload["no_of_guests"] = 5
        updated = self.client.put(f"/api/tables/{pk}/", payload, format="json")
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(Booking.objects.get(pk=pk).no_of_guests, 5)

        self.assertEqual(self.client.delete(f"/api/tables/{pk}/").status_code, 204)


class RegistrationAndTokenTest(TestCase):
    def test_register_and_login(self):
        client = APIClient()
        reg = client.post(
            "/auth/users/", {"username": "newuser", "password": "Str0ngPass!234"}, format="json"
        )
        self.assertEqual(reg.status_code, 201)
        login = client.post(
            "/auth/token/login/", {"username": "newuser", "password": "Str0ngPass!234"}, format="json"
        )
        self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token", login.data)


class StaticPagesTest(TestCase):
    def test_home_page(self):
        self.assertContains(self.client.get("/"), "Little Lemon")

    def test_menu_page(self):
        Menu.objects.create(title="Greek Salad", price=12, inventory=10)
        self.assertContains(self.client.get("/menu/"), "Greek Salad")
