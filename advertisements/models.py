from django.db import models
from companies.models import CompanyProfile

import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

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


STATUS = ((1, "Pending"), (0, "Complete"))

class Transaction(models.Model):
    """This model records all the mpesa payment transactions"""
    transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return f"{self.transaction_no}"
