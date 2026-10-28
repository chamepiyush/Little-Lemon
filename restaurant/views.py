from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer


# ----------------------------------------------------- Static HTML (Django)
def index(request):
    return render(request, "index.html", {})


def menu_page(request):
    items = Menu.objects.all().order_by("title")
    return render(request, "menu.html", {"menu": items})


# --------------------------------------------------------------- Menu API
class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


# ------------------------------------------------------------ Booking API
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
