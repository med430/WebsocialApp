from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Profile, Avatar
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:login"))
    if request.method == "POST":
        user = request.user
        text = request.POST["text"]
        image = request.FILES.get("image")

        if image:
            if image.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                return render(request, "media/index.html", {
                    "message": "The file is not an image or the image type is not supported"
                })
            if image.size > 200 * 1024 * 1024:
                return render(request, "media/index.html", {
                    "message": "Image too large larger than 200mb"
                })
            
        if text or image:
            post = Post(author=user, text=text, image=image)
            post.save()
            return HttpResponseRedirect(reverse("media:index"))
        else:
            return render(request, "media/index.html", {
                "message": "The post mustn't be empty"
            })
    return render(request, "media/index.html", {
        "username": request.user.username
    })

def user_posts(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:login"))
    return render(request, "media/user_posts.html", {
        "username": User.objects.get(id=user_id),
        "user_id": user_id
    })

def profile(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:login"))
    if request.method == "POST":
        user = request.user
        if user.id == user_id:
            avatar = request.FILES.get("avatar")
            if avatar:
                if avatar.content_type not in ["image/jpeg", "image/png", "image/gif"]:
                    return render(request, "media/profile.html", {
                        "username": User.objects.get(id=user_id),
                        "user_id": user_id,
                        "message": "the uploaded file is not an image or the image type is not supported"
                    })
                if avatar.size > 200 * 1024 * 1024:
                    return render(request, "media/profile.html", {
                        "username": User.objects.get(id=user_id),
                        "user_id": user_id,
                        "message": "Image too large larger than 200mb"
                    })
                
                avatar_obj = Avatar(user_id=user_id, avatar=avatar)
                avatar_obj.save()
                return HttpResponseRedirect(reverse("media:user_profile", kwargs={'user_id': user_id}))
            return render(request, "media/profile.html", {
                "username": User.objects.get(id=user_id),
                "user_id": user_id,
                "message": "There are no changes"
            })
        return HttpResponseRedirect(reverse("media:user_profile", kwargs={'user_id': user_id}))
    return render(request, "media/profile.html", {
        "username": User.objects.get(id=user_id),
        "user_id": user_id
    })

def avatars(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:login"))
    return render(request, "media/avatars.html", {
        "username": User.objects.get(id=user_id),
        "user_id": user_id
    })