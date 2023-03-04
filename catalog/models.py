from django.db import models
from companies.models import CompanyProfile


class Catalog(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='catalogs')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Catalogs'

        

# create model for catalog categories
class CatalogCategory(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Catalog Categories'

# create model for catalog items
class CatalogItem(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    category = models.ForeignKey(CatalogCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/catalog/', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Catalog Items'

