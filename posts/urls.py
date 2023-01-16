from django.urls import path
from . import views
urlpatterns = [
     path('<str:id>/', views.allPosts, name='allPosts'),
     path('add_post/<str:id>/', views.add_post, name='add_post'),
]