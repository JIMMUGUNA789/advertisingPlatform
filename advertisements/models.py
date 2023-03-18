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


    # M-pesa payment


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
# M-pesa Payment models
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'
class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'
class MpesaPayment(BaseModel):
    ad_id = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad', default=1)
    amount = models.IntegerField()
    phone_number =models.CharField(max_length=100)
    mpesa_receipt_number = models.CharField(max_length=100, null=True, blank=True)
    transaction_date = models.DateTimeField( null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.TextField( null=True, blank=True)
    reference = models.TextField(   null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
    def __str__(self):
        return self.first_name



