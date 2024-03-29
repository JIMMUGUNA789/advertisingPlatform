from django.urls import path
from . import views
# url patterns for the catalog app
urlpatterns = [
    path('ads/<int:ad_id>/', views.ad_click, name='adclick'),
    path('ads/impressions/<int:ad_id>/', views.show_ad, name='adimpression'),
    path('ads/delete/<int:ad_id>/', views.deleteAd, name='deleteAd'),
    path('ads/create/<int:company_id>/', views.createAd, name='createAd'),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa/<str:ad_id>', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
        # register, confirmation, validation and callback urls
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation/', views.paymentConfirmation, name="confirmationUrl"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.call_back, name="call_back"),
    # simulate transaction
    path('c2b/simulate/<str:ad_id>', views.simulate, name="simulate"),
    
    
]