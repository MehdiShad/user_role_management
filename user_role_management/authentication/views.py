from django.http import HttpRequest
from django.contrib.auth import logout
from rest_framework import serializers
from rest_framework.views import APIView, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from user_role_management.core.exceptions import success_response, error_response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

@extend_schema(tags=['Authentication'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['Authentication'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Authentication'])
class CustomTokenVerifyView(TokenVerifyView):
    pass

@extend_schema(tags=['Authentication'])
class CustomTokenBlacklistView(TokenBlacklistView):
    pass


class LogoutApi(APIView):

    class InputLogoutSerializer(serializers.Serializer):
        refresh_token = serializers.CharField(max_length=255)

    class OutputLogoutSerializer(serializers.Serializer):
        is_success = serializers.BooleanField(default=True)

    @extend_schema(request=InputLogoutSerializer, responses=OutputLogoutSerializer, tags=['Authentication'])
    def post(self, request: HttpRequest):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response(error_response(message='Refresh token is required'), status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(refresh_token).blacklist()
            return Response(success_response(), status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(error_response(message=str(ex)), status=status.HTTP_400_BAD_REQUEST)

