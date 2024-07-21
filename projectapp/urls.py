from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signuppage'),
    path('login/', login_view, name='loginpage'),
    path('logout', logout_view, name='logoutuser'),
    path('', home, name='home'),
]