from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .models import Room, Amenity
from categories.models import Category
from .serializer import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)

class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] #IsAuthenticatedOrReadOnly는 인증된 사용자에게는 읽기/쓰기 권한을 부여하고, 인증되지 않은 사용자에게는 읽기 권한만 부여하는 권한 클래스

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try: 
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic(): #transaction.atomic()을 사용하여 데이터베이스 트랜잭션을 시작. 이 블록 내에서 발생하는 모든 데이터베이스 작업은 하나의 트랜잭션으로 묶임. 만약 블록 내에서 예외가 발생하면, 모든 변경 사항이 롤백되어 데이터베이스가 이전 상태로 되돌아감.
                    room = serializer.save(owner=request.user, category=category)  #request.user를 통해 현재 로그인한 사용자를 가져와서 방의 owner로 설정. 
                    amenities = request.data.get("amenities")                      #해당 owner 정보를 포함한 RoomDetailSerializer를 사용하여 방의 상세 정보를 직렬화
                    for amenity_pk in amenities: #amenity에 없는 정보를 입력시, 오류가 발생하게 설정. (예외처리)
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)  #room 객체에 amenity를 추가
                    serializer = RoomDetailSerializer(room) #RoomDetailSerializer를 사용하여 방의 상세 정보를 직렬화
                    return Response(serializer.data) #직렬화된 데이터를 응답으로 반환
            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(serializer.errors)

class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] #IsAuthenticatedOrReadOnly는 인증된 사용자에게는 읽기/쓰기 권한을 부여하고, 인증되지 않은 사용자에게는 읽기 권한만 부여하는 권한 클래스

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
class RoomReviews(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound    

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room=self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True)
        return Response(serializer.data)

class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] #IsAuthenticatedOrReadOnly는 인증된 사용자에게는 읽기/쓰기 권한을 부여하고, 인증되지 않은 사용자에게는 읽기 권한만 부여하는 권한 클래스

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)
        # Handle photo upload logic here
        return Response({"message": "Photo uploaded successfully."})


"""
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(request, "all_rooms.html", 
                  {
                      "rooms": rooms,
                      "title": "Hello! this title comes from django",
                      },
    )

def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
"""
