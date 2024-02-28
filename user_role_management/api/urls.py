from django.urls import path, include

urlpatterns = [
    path('auth/', include(('user_role_management.authentication.urls', 'auth'))),
    path('manage/', include(('user_role_management.manage.urls', 'manage'))),
]
