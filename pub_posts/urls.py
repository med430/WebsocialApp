from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AllPostsViewSet, PostsAPI, LikePost, CommentPost, ProfileAPI, AvatarAPI, like, unlike, comment

router = DefaultRouter()
router.register(r'all-posts', AllPostsViewSet, basename="all-posts")

app_name = "api"

urlpatterns = [
    path('', include(router.urls)),
    path('profile/<int:user_id>', ProfileAPI.as_view(), name="profile"),
    path('profile/avatars/<int:user_id>', AvatarAPI.as_view(), name="avatar"),
    path('posts/<int:user_id>', PostsAPI.as_view(), name="posts"),
    path('likes-posts/like/<int:post_id>', like, name="like"),
    path('likes-posts/unlike/<int:post_id>', unlike, name="unlike"),
    path('likes/<int:post_id>', LikePost.as_view(), name="likes"),
    path('comments/<int:post_id>', comment, name="comment"),
    path('all-comments/<int:post_id>', CommentPost.as_view(), name="comments")
]