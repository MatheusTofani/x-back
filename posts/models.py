from django.db import models
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    retweet_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='retweets')

    def __str__(self):
        if self.retweet_post:
            return f"{self.user.username} retweetou {self.retweet_post.id}"
        return f"{self.user.username}: {self.content[:50]}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  
    def __str__(self):
        return f"{self.user.username} curtiu post {self.post.id}"
