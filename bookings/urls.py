from django.urls import path
from . import views

urlpatterns = [
    path("", views.Bookings.as_view()),
    path("rooms", views.RoomBookings.as_view()),
    path("experiences", views.ExperienceBooking.as_view()),
]