from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking
from .serializers import (
    PublicBookingSerializer,
    CreateRoomBookingSerializer,
    CreateExperienceBookingSerializer,)

# Create your views here.
class Bookings(APIView):
    def get(self, request):
        now = timezone.localtime(timezone.now())
        bookings = Booking.objects.filter(
            check_out__gte=now.date()
        ).order_by("check_in")
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

class RoomBookings(APIView):
    def post(self, request):
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ExperienceBooking(APIView):
    def post(self, request):
        experience = request.data.get("experience")
        serializer = CreateExperienceBookingSerializer(
            data=request.data, context={"experience": experience}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)