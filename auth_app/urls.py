# auth_app/urls.py

from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'auth_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
]
