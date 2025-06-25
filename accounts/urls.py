from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserCreateView, UserUpdateView, recent_users


urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/edit/', UserUpdateView.as_view(), name='profile-edit'),
    path('users/recent/', recent_users, name='recent-users'),
]
