from django.urls import path

from . import views

app_name = "sign_in"

urlpatterns = [
    path('', views.index, name = "index"),
    path('login', views.login_view, name="login"),
    path('sign_up', views.sign_up, name = "sign_up"),
    path('logout', views.logout_view, name="logout"),
    path('user', views.user, name="user")
]