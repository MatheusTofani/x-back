from django.urls import path
from .views import FollowUserView,  FollowersCountView, IsFollowingView

urlpatterns = [
    path('<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('<str:username>/followers-count/', FollowersCountView.as_view(), name='followers-count'),
    path('<str:username>/is-following/', IsFollowingView.as_view(), name='is-following'),
]