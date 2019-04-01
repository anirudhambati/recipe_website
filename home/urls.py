from django.urls import path, include
from . import views
app_name='home'

urlpatterns = [
    path('', views.explore),
    path('recipe', views.recipe),

]
