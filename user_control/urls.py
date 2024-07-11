from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user_control.views.auth import (
    LoginAPIView, LogoutAPIView, PasswordChangeAPIView, PasswordResetAPIView, RegisterAPIView,
    RequestPasswordResetAPIView,
)
from user_control.views.user import (
    GetUserListAPIView, CreateUserAPIView, GetUserDetailsAPIView, UpdateUserDetailsAPIView, GetUserProfileAPIView,
)

urlpatterns = [
    # Auth URLs
    path('auth/register/', RegisterAPIView.as_view()),
    # path('auth/verify-email/', VerifyEmailAPIView.as_view(), name="verify-email"),
    # path('auth/resend-verification-email/', ResendVerificationEmailAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/logout/', LogoutAPIView.as_view(), name="logout"),
    path('auth/password-change/', PasswordChangeAPIView.as_view(), name="password_change"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/request-password-reset/', RequestPasswordResetAPIView.as_view(), name="request_password_reset"),
    path('auth/password-reset/<uidb64>/<token>/', PasswordResetAPIView.as_view(), name='password_reset_confirm'),

    # User URLs
    path('user/list/', GetUserListAPIView.as_view(), name='get_user_list'),
    path('user/create/', CreateUserAPIView.as_view(), name='create_user'),
    path('user/profile/', GetUserProfileAPIView.as_view(), name='get_user_profile'),
    path('user/<str:pk>/details/', GetUserDetailsAPIView.as_view(), name='get_user_details'),
    path('user/<str:pk>/update/', UpdateUserDetailsAPIView.as_view(), name='update_user_details'),
]
