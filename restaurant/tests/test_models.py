from datetime import datetime, timezone
from decimal import Decimal

from django.test import TestCase

from restaurant.models import Booking, Menu


class MenuModelTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=Decimal("80.00"), inventory=100)
        self.assertEqual(str(item), "IceCream : 80.00")


class BookingModelTest(TestCase):
    def test_create_booking(self):
        booking = Booking.objects.create(
            name="Anna",
            no_of_guests=4,
            booking_date=datetime(2026, 12, 1, 19, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(str(booking), "Anna")
        self.assertEqual(Booking.objects.count(), 1)
