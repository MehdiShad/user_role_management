from django.urls import path, include

urlpatterns = [
    path('auth/', include(('user_role_management.authentication.urls', 'auth'))),
    path('users/', include(('user_role_management.users.urls', 'users'))),
]
