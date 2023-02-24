from django.urls import path
from . import views
# url patterns for the catalog app
urlpatterns = [
    path('ads/<int:ad_id>/', views.ad_click, name='adclick'),
    path('ads/impressions/<int:ad_id>/', views.show_ad, name='adimpression'),
    
]