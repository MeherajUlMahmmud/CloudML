from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from user_control.views.auth import LoginAPIView, LogoutAPIView
from user_control.views.user import UserModelViewSet

router = routers.DefaultRouter()
router.register(r'user', UserModelViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api/auth/login/', LoginAPIView.as_view(), name="login"),
    path('api/auth/logout/', LogoutAPIView.as_view(), name="logout"),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
