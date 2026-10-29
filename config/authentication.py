from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from multiprocessing import AuthenticationError
from users.models import User
import jwt
from django.conf import settings

class TrustAuthentication(BaseAuthentication): 
#Header를 통한 인증 (Header key값이 없는 경우 -> 로그아웃 처리/ Hedaer key값으로 User find -> 로그인 시도/ User 존재하는 경우 -> 로그인 성공/ User 존재하지 않는 경우 -> 로그인 실패)
    def authenticate(self, request):
        username = request.headers.get("secretuser")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"{username} not found")

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        if not token:
            return None
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"],)
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")
