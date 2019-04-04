from django.urls import path, include
from . import views
app_name='home'

urlpatterns = [
    path('', views.home),
    path('explore', views.explore),
    path('recipe/<id>', views.recipe,name='recipe'),
    path('register',views.register,name='register'),
    path('registered',views.registered,name='registered'),
    path('login',views.login,name='login'),
    path('base', views.base, name='base'),
    path('search',views.search,name='search'),
]
