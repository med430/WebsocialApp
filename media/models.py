import os
import uuid
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('media/static/images/posts/', unique_filename)

def get_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('media/static/images/avatars/', unique_filename)

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=False, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"profile picture of {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_image_path , blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ch = self.content if len(self.content)<=30 else ch[:30] + "..."
        return f"{self.author.username}: {ch}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ch = self.content if len(self.content)<=30 else ch[:30] + "..."
        return f"{self.author.username}: {ch}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    liked = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"