from django.urls import path
from . import views
# url patterns for the catalog app
urlpatterns = [
    path('create-catalog/<str:company_id>', views.createCatalog, name='createCatalog'),
    path('delete-catalog/<str:catalog_id>', views.deleteCatalog, name='deleteCatalog'),
    path('manage-catalog/<str:catalog_id>',views.manageCatalog, name='manageCatalog'),
    path('create-catalog-category/<str:catalog_id>', views.createCatalogCategory, name='createCatalogCategory'),
    path('delete-catalog-category/<str:category_id>', views.deleteCatalogCategory, name='deleteCatalogCategory'),
]
