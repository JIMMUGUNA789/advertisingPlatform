from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('<str:id>/profile/', views.companyProfile, name='companyProfile'),
    path('<pk>/profile/update/', views.CompanyProfileUpdate.as_view(), name='updateCompanyProfile'),
    path('<str:id>/photos/', views.companyPhotos, name='companyPhotos'),
    path('<str:id>/add-images/', views.addImages, name='addImages'),
    path('<str:id>/reviews/', views.reviews, name= 'reviews' ),
    path('list-company/', views.listCompany, name='listCompany'),
    path('<str:id>/add_review/', views.addReview, name='add_review'),
    path('likeAndDislikeCompany/<str:company_id>/', views.likeAndDislikeCompany, name='likeAndDislikeCompany'),
    path('followAndUnfollowCompany/<str:company_id>/', views.followAndUnfollowCompany, name='followAndUnfollowCompany'),
    path('digiverse/', views.digiverseSite, name='digiverse'),
    path('contact/<str:company_id>/', views.contactCompany, name='contact'),
    path('terms-of-use/', views.termsOfUse, name='termsOfUse'),
]