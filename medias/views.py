from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from .models import Photo

# Create your views here.
class PhotoDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly] #IsAuthenticatedOrReadOnly는 인증된 사용자에게는 읽기/쓰기 권한을 부여하고, 인증되지 않은 사용자에게는 읽기 권한만 부여하는 권한 클래스

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
            ):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)
