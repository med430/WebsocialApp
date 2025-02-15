from rest_framework import viewsets, filters, generics, pagination, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from media.models import Post, Like, Comment, Profile, Avatar
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, ProfileSerializer, AvatarSerializer
from .permissions import IsAdminOrReadOnly

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user

    like, created = Like.objects.get_or_create(post=post, user=user)

    if like.liked:
        return Response({'detail': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)
    
    like.liked = True
    like.save()
    return Response({'detail': 'Post liked'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    
    like, created = Like.objects.get_or_create(post=post, user=user)

    if not like.liked:
        return Response({'detail': 'already unliked'}, status=status.HTTP_400_BAD_REQUEST)
    
    like.liked = False
    like.save()
    return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    author = request.user
    content = request.data.get("content")
    
    if content:
        comment = Comment(post=post, author=author, content=content)
        comment.save()
        return Response({'detail': 'comment published'}, status=status.HTTP_200_OK)
    
    return Response({'detail': 'comment not holding any content'}, status=status.HTTP_400_BAD_REQUEST)

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomLikePagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class AllPostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-creation_date')
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

class PostsAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Post.objects.filter(author_id=user_id).order_by('-creation_date')

class LikePost(generics.ListAPIView):
    serializer_class = LikeSerializer
    pagination_class = CustomLikePagination
    
    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Like.objects.filter(post_id=post_id, liked=True)

class CommentPost(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id).order_by('-creation_date')

class ProfileAPI(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Profile.objects.filter(user_id=user_id)

class AvatarAPI(generics.ListAPIView):
    serializer_class = AvatarSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Avatar.objects.filter(user_id=user_id).order_by('-creation_date')