from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from media.models import Profile

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:login"))
    return HttpResponseRedirect(reverse("sign_in:user"))

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:user"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("sign_in:user"))
        else:
            return render(request, "user/login.html", {
                "message": "Invalid credentials."
            })
    return render(request, "user/login.html")

def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:user"))
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user)
            profile.save()
            login(request, authenticate(request, username=request.POST["username"], password=request.POST["password1"]))
            return HttpResponseRedirect(reverse("sign_in:user"))
        return render(request, "user/sign_up.html", {
            'form': UserCreationForm().as_p(),
            'message': 'username or email already exists.'
        })
    return render(request, "user/sign_up.html", {
        'form': UserCreationForm().as_p()
    })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse("sign_in:login"))

def user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sign_in:login"))
    return render(request, "user/user.html", {
        "username": request.user.username,
        "email": request.user.email,
        "user_id": request.user.id
    })