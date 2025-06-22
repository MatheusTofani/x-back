from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        
User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'bio', 'followers', 'following']

    def get_followers(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_following(self, obj):
        return Follow.objects.filter(follower=obj).count()