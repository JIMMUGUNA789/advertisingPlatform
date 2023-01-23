from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("profile/<str:id>/", views.profile, name="profile"),
    path("profile/<int:pk>/edit/", views.UserUpdate.as_view(), name="edit_profile"),
    path("businessDashboard/<str:user_id>/<str:company_id>/", views.businessDashboard, name="businessDashboard"),
]