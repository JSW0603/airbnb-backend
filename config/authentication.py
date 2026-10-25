from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

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