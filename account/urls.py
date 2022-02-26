from django.urls import path
from .views import home, SignUp, login_view, log_out

urlpatterns = [
    path('', home, name="home"),
    path("signup/", SignUp.as_view(), name="signup"),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='log_out')
]
