from rest_framework import serializers
from media.models import Post, Like, Comment, Profile, Avatar

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'username', 'content', 'creation_date']
    
    def get_username(self, obj):
        return obj.author.username

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Like
        fields = ['id', 'username']
    
    def get_username(self, obj):
        return obj.user.username

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    likes_number = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'username', 'text', 'image', 'creation_date', 'liked_by_user', 'likes_number']
    
    def get_username(self, obj):
        return obj.author.username
    
    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        if Like.objects.filter(post=obj, user=user).exists():
            return Like.objects.get(post=obj, user=user).liked
        return False
    
    def get_likes_number(self, obj):
        return Like.objects.filter(post=obj, liked = True).count()

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id', 'username', 'bio']
    
    def get_username(self, obj):
        return obj.user.username

class AvatarSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Avatar
        fields = ['id', 'username', 'avatar', 'creation_date']
    
    def get_username(self, obj):
        return obj.user.username