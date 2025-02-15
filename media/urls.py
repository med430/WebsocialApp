from django.urls import path

from . import views

app_name = "media"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:user_id>', views.user_posts, name="user_posts"),
    path('profile/<int:user_id>', views.profile, name="user_profile"),
    path('profile/avatars/<int:user_id>', views.avatars, name="avatars")
]