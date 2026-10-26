from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .serializer import PrivateUserSerializer
import jwt

# Create your views here.
class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer_private = PrivateUserSerializer(user)
        return Response(serializer_private.data)

    def put(self, request):
        user = request.user
        serializer_private = PrivateUserSerializer(
            user, data=request.data, partial=True,
        )
        if serializer_private.is_valid():
            user = serializer_private.save()
            serializer_private = PrivateUserSerializer(user)
            return Response(serializer_private.data)
        else:
            return Response(serializer_private.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        serializer_User = PrivateUserSerializer(data=request.data)
        if serializer_User.is_valid():
            user = serializer_User.save()
            user.set_password(password)
            user.save()
            serializer_User = PrivateUserSerializer(user)
            return Response(serializer_User.data)
        else:
            return Response(serializer_User.errors)

class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User not found.")
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Username and password are required.")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"ok": "Welcome back!"})
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Logged out successfully."})

class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "Invalid credentials."})