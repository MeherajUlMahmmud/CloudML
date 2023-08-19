from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from user_control.urls import router as user_router
from model_control.urls import router as model_router

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(model_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('user_control.urls')),
    path('', include('model_control.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.DATA_ROOT)

