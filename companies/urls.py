from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('<str:id>/profile/', views.companyProfile, name='companyProfile'),
    path('<str:id>/photos/', views.companyPhotos, name='companyPhotos'),
    path('<str:id>/reviews/', views.reviews, name= 'reviews' ),
    path('list-company/', views.listCompany, name='listCompany'),
    path('<str:id>/add_review/', views.addReview, name='add_review'),
]