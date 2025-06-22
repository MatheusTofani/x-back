
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Follow

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, username):
        target = get_object_or_404(User, username=username)
        if target == request.user:
            return Response({"detail": "Não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if created:
            return Response({"detail": f"Agora segue {username}."}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Já segue."}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, username):
        target = get_object_or_404(User, username=username)
        obj = Follow.objects.filter(follower=request.user, following=target).first()
        if obj:
            obj.delete()
            return Response({"detail": f"Deixou de seguir {username}."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Não seguia."}, status=status.HTTP_404_NOT_FOUND)

class FollowersCountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        followers = Follow.objects.filter(following=user).count()
        following = Follow.objects.filter(follower=user).count()
        return Response({"followers": followers, "following": following})

class IsFollowingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
        return Response({"is_following": is_following})
