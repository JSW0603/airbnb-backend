from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializer

# Create your views here.
class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer_private = serializer.PrivateUserSerializer(user)
        return Response(serializer_private.data)

    def put(self, request):
        user = request.user
        serializer_private = serializer.PrivateUserSerializer(
            user, data=request.data, partial=True,
        )
        if serializer_private.is_valid():
            user = serializer_private.save()
            serializer_private = serializer.PrivateUserSerializer(user)
            return Response(serializer_private.data)
        else:
            return Response(serializer_private.errors)


