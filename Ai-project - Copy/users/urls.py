from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),   
    path('user_login/', views.Userlogin, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]