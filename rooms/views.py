from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Amenity
from categories.models import Category
from .serializer import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT

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
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:  #허용된 사용자만 방을 생성할 수 있도록 설정
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try: 
                    category = category.objects.get(pk=category_pk)
                    if category.kind == category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'.")
                except category.DoesNotExist:
                    raise ParseError("Category not found.")
                room = serializer.save(owner=request.user, category=category)  #request.user를 통해 현재 로그인한 사용자를 가져와서 방의 owner로 설정. 
                amenities = request.data.get("amenities")                      #해당 owner 정보를 포함한 RoomDetailSerializer를 사용하여 방의 상세 정보를 직렬화
                for amenity_pk in amenities: #amenity에 없는 정보를 입력시, 오류가 발생하게 설정. (예외처리)
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        raise ParseError(f"Amenity with id {amenity_pk} not found.")

                    
                serializer = RoomDetailSerializer(room)                        
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated

class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
    

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
