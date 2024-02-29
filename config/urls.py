from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_spectacular.settings import spectacular_settings


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/v1/', include(('user_role_management.api.urls', 'api'))),
]

if settings.DEBUG:
    spectacular_settings.SWAGGER_UI_SETTINGS = {
        'deepLinking': True,
        'docExpansion': 'none',
        'defaultModelsExpandDepth': -1,
        'displayOperationId': False,
    }

    urlpatterns += [
        path("docs/swagger-ui", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
        path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)