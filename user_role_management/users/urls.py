from django.urls import path
from user_role_management.users.apis import register, process


urlpatterns = [
    path('register/', register.RegisterApi.as_view(), name="register"),
    path('processes/', process.ProcessesApi.as_view(), name="processes"),
]
