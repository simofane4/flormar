from django.urls import path
from .views.users import phone_login ,home ,user_list
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', phone_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path('user_list/', user_list, name='user_list'),
]
