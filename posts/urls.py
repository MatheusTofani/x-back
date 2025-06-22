from django.urls import path
from .views import PostListCreateView, LikePostView, PostDetailView, PublicUserProfileView, RetweetPostView, UserPostsView, UserRetweetsView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='posts-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:post_id>/retweet/', RetweetPostView.as_view(), name='retweet-post'),
    path('users/<str:username>/retweets/', UserRetweetsView.as_view(), name='user-retweets'),
    path('users/<str:username>/info/', PublicUserProfileView.as_view(), name='public-user-profile'),
    path('users/<str:username>/posts/', UserPostsView.as_view(), name='user-posts'),
]
