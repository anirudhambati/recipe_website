from django.urls import path, include
from . import views
app_name='home'

urlpatterns = [
    path('', views.explore),
    path('recipe', views.recipe,name='recipe'),
    path('register',views.register,name='register'),
    path('registered',views.registered,name='registered'),
    path('login',views.login,name='login'),
]
