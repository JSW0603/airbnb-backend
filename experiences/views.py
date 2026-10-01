from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Content, Experience
from categories.models import Category
from .serializers import ContentSerializer, ExperienceSerializer, ExperienceDetailSerializer
from bookings.models import Booking
from bookings.serializers import CreateRoomBookingSerializer, PublicBookingSerializer, CreateExperienceBookingSerializer


# Create your views here.
class Contents(APIView):
    def get(self, request):
        all_contents = Content.objects.all()
        serializer = ContentSerializer(all_contents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response(ContentSerializer(content).data)
        else:
            return Response(serializer.errors)

class ContentDetail(APIView):
    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def put(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            updated_content = serializer.save()
            return Response(ContentSerializer(updated_content).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete
        return Response(status=HTTP_204_NO_CONTENT)

class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(all_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.CategoryKindChoices.EXPERIENCE:
                    raise ParseError("The category kind should be 'experience'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)
                    contents = request.data.get("contents")
                    for content in contents:
                        content_obj = Content.objects.get(pk=content)
                        experience.contents.add(content_obj)
                    serializer = ExperienceSerializer(experience)
                    return Response(ExperienceDetailSerializer(experience).data)
            except Exception:
                raise ParseError("Content not found.")
        else:
            return Response(serializer.errors)                    

class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = ExperienceDetailSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("Category kind should be 'experience'.")
            except Category.DoesNotExist:
                raise NotFound("Category not found.")

            content_pks = request.data.get("contents")
            contents = []
            if not content_pks:
                content_pks = []
            try:
                for content_pk in content_pks:
                    content = Content.objects.get(pk=content_pk)
                    contents.append(content)
            except Content.DoesNotExist:
                raise ParseError("Contents are required.")

            updated_experience = serializer.save(
                category=category, contents=contents)
            return Response(ExperienceDetailSerializer(updated_experience).data)
        else:
            raise Response(serializer.errors)
            

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound ("Experience not found.")

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(experience=experience, 
                                          kind=Booking.BookingChoices.EXPERIENCE, 
                                          experience_time__gte=now)
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data,
                                                 context={"experience": experience})
        if serializer.is_valid():
            booking = serializer.save(
                user=request.user,
                kind=Booking.BookingChoices.EXPERIENCE,
                experience=experience,
            )
            return Response(PublicBookingSerializer(booking).data)
        else:
            return Response(serializer.errors)
        
class ExperienceBooking(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound("Experience not found.")

    def get(self, pk, experience):
        try:
            return Booking.objects.get(
                experience=experience,
                kind=Booking.BookingChoices.EXPERIENCE,
                pk=pk,)
        except Booking.DoesNotExist:
            raise NotFound("Booking not found.")

    def get(self, request, pk, booking_pk):
        experience = self.get_object(pk)
        booking = self.get_booking(booking_pk, experience)
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)

    def delete(self, request, pk, booking_pk):
        experience = self.get_object(pk)
        booking = self.get_booking(booking_pk, experience)
        booking.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk, booking_pk):
        if request.data.get("check_in") or request.data.get("check_out"):
            raise ParseError("You cannot change check-in or check-out dates.")

        experience = self.get_object(pk)
        booking = self.get_booking(booking_pk, experience)
        serializer = CreateExperienceBookingSerializer(
            booking,
            data=request.data,
            context={"experience": experience},
            partial=True,
        )
        if serializer.is_valid():
            updated_booking = serializer.save()
            return Response(PublicBookingSerializer(updated_booking).data)
        else:
            return Response(serializer.errors)