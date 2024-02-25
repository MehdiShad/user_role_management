from . import views
from django.urls import path, include

urlpatterns = [
        path('jwt/', include(([
            path('login/', views.CustomTokenObtainPairView.as_view(), name="login"),
            path('logout/', views.CustomTokenBlacklistView.as_view(), name="logout"),
            path('refresh/', views.CustomTokenRefreshView.as_view(), name="refresh"),
            path('verify/', views.CustomTokenVerifyView.as_view(), name="verify"),
            ])), name="jwt"),
]
