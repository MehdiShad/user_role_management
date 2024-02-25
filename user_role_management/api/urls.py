from django.urls import path, include

urlpatterns = [
    path('auth/', include(('usermanagement.authentication.urls', 'auth'))),
    path('users/', include(('usermanagement.users.urls', 'users'))),
]
