from django.urls import path, include

urlpatterns = [
    path('auth/', include(('user_role_management.authentication.urls', 'auth'))),
    path('user_management/', include(('user_role_management.users.urls', 'user_management'))),
]
