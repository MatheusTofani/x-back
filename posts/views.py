from rest_framework import generics
from .models import Post, Like
from .serializers import PostSerializer
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({"detail": "Post não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({"detail": "Post curtido."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Você já curtiu este post."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        like = Like.objects.filter(user=request.user, post_id=post_id).first()
        if like:
            like.delete()
            return Response({"detail": "Curtida removida."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Curtida não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
class PostDetailView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            raise PermissionDenied("Você não tem permissão para deletar este post.")
        return super().delete(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

    
class RetweetPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        original_post = get_object_or_404(Post, id=post_id)

        
        if Post.objects.filter(user=request.user, retweet_post=original_post).exists():
            return Response({"detail": "Você já retweetou este post."}, status=400)

        Post.objects.create(user=request.user, retweet_post=original_post)
        return Response({"detail": "Retweet feito com sucesso."}, status=201)


class PublicUserProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserPostsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=user, retweet_post__isnull=True).order_by("-created_at")
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class UserRetweetsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=user, retweet_post__isnull=False).order_by("-created_at")
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)