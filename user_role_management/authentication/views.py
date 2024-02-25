from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView



@extend_schema(tags=['Authentication'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['Authentication'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Authentication'])
class CustomTokenVerifyView(TokenVerifyView):
    pass
