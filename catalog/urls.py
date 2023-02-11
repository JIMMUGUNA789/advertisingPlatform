from django.urls import path
from . import views
# url patterns for the catalog app
urlpatterns = [
    path('create-catalog/<str:company_id>', views.createCatalog, name='createCatalog'),
    path('delete-catalog/<str:catalog_id>', views.deleteCatalog, name='deleteCatalog'),
]
