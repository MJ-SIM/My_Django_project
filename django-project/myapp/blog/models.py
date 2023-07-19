from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default = '')
    content = models.TextField()
    writer = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)