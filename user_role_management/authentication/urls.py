from . import views
from django.urls import path, include

urlpatterns = [
        path('jwt/', include(([
            path('login/', views.TokenObtainPairView.as_view(), name="login"),
            path('refresh/', views.TokenRefreshView.as_view(), name="refresh"),
            path('verify/', views.TokenVerifyView.as_view(), name="verify"),
            ])), name="jwt"),
]
