from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home,name='forum-home'),
    path('insert/',views.insert,name = 'insert'),
    path('search/',views.search,name = 'search'),
    path('insert1/',views.insert1,name = 'insert1'),
]