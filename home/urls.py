from django.urls import path, include
from . import views
app_name='home'

urlpatterns = [
    path('', views.explore),
    path('recipe', views.recipe),
    path('register',views.register),
    path('registered',views.registered,'registered'),
    path('login',views.login,name='login'),
]
