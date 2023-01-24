from django.urls import path
from . import views
urlpatterns = [
     path('<str:id>/', views.allPosts, name='allPosts'),
     path('add_post/<str:id>/', views.add_post, name='add_post'),
     path('likeAndDislikePost/<str:post_id>/<str:company_id>/', views.likeAndDislikePost, name='likeAndDislikePost'),
     path('deletePost/<str:post_id>/<str:company_id>/', views.deletePost, name='deletePost'),
     path('addComment/<str:post_id>/<str:company_id>/', views.addComment, name='addComment'),
     path('all-comments/<str:post_id>/<str:company_id>/', views.postComments, name='allComments'),
     path('deleteComment/<str:comment_id>/<str:company_id>/<str:post_id>/', views.deleteComment, name='deleteComment'),
]