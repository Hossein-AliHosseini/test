from django.urls import path
from .views import home, signup_view, login_view, log_out, change_password

urlpatterns = [
    path('', home, name="home"),
    path("signup/", signup_view, name="signup"),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='log_out'),
    path('changepassword/', change_password, name='change_password'),
]
