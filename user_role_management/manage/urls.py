from django.urls import path
from user_role_management.manage.apis.v1 import user, process


urlpatterns = [
    path('register/', user.RegisterApi.as_view(), name="register"),
    path('processes/', process.ProcessesApi.as_view(), name="processes"),
]
