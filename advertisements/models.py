from django.db import models
from companies.models import CompanyProfile

class Ad(models.Model):
    companyProfile = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='advertisements')
    adImage = models.ImageField(upload_to='ads')
    Ad_text = models.CharField(max_length=100 , blank=True)
    AD_TYPE_CHOICES = [
        ('Banner', 'Banner'),
        ('Sidebar', 'Sidebar'),
        ('Footer', 'Footer')
    ]
    adType = models.CharField(choices=AD_TYPE_CHOICES, max_length=50)
    AD_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    adStatus = models.CharField(choices=AD_STATUS_CHOICES, max_length=50, default='Inactive')
    impressionsCount = models.PositiveIntegerField(default=0)
    clicksCount = models.PositiveIntegerField(default=0)
    startDate = models.DateField()
    endDate = models.DateField()
