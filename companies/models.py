from django.db import models
from users.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import datetime
# from django.contrib.gis.db import models
class CompanyProfile(models.Model):
    CATEGORY_CHOICES = (
        ('Agriculture','Agriculture'),
        ('Mining','Mining'),
        ('Manufacturing', 'Manufacturing'),
        ('Construction', 'Construction'),
        ('Wholesale and Retail', 'Wholesale and Retail'),
        ('Transport','Transport'),
        ('Hospitality','Hospitality'),
        ('Technology', 'Technology'),
        ('Finance', 'Finance'),
        ('Real Estate', 'Real Estate'),
        ('Education','Education'),
        ('Health', 'Health'),
        ('Entertainment','Entertainment'),
        ('Others', 'Others')
    )
    companyName = models.CharField(max_length=255)
    companyAdmin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    profilePicture = models.ImageField(upload_to='media/', blank=True)
    bannerPicture = models.ImageField(upload_to='media/', blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=255, default='Others')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    websiteUrl = models.URLField()
    latitude = models.FloatField(default=0.0, blank=True, null=True)
    longitude = models.FloatField(default=0.0, blank=True, null=True)
    address = models.CharField(max_length=255)
    operatingHours = models.JSONField(default={'key': 'value'})
    companyLikes = models.IntegerField(default=0)
    companyFollows = models.IntegerField(default=0)
    companyReviews = models.IntegerField(default=0)
    
    

    # how the operating hours will be stored
#     business = Business.objects.get(id=1)
#     business.hours = {
#     'Monday': {'open': '09:00:00', 'close': '17:00:00'},
#     'Tuesday': {'open': '09:00:00', 'close': '17:00:00'},
#     'Wednesday': {'open': '09:00:00', 'close': '17:00:00'},
#     'Thursday': {'open': '09:00:00', 'close': '17:00:00'},
#     'Friday': {'open': '09:00:00', 'close': '17:00:00'},
# }
# business.save()

    def __str__(self):
        return self.companyName
    class Meta:
        verbose_name_plural = 'Company Profiles'

class Follows(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE) 
    def __str__(self):
        return self.company.companyName
    class Meta:
        verbose_name_plural = 'Follows'

class Likes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.company.companyName
    class Meta:
        verbose_name_plural = 'Likes'


class Reviews(models.Model):
    RATING_CHOICES = (
        
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)

    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    reviewPhoto = models.ImageField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.company.companyName
    class Meta:
        verbose_name_plural = 'Reviews'

class CompanyImages(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    def __str__(self):
        return self.company.companyName
    class Meta:
        verbose_name_plural = 'Company Images'


@receiver(post_save, sender=Likes)
def increment_company_likes(sender, instance, created, **kwargs):
    if created:
        companyProfile = CompanyProfile.objects.get(pk=instance.company.pk)
        companyProfile.companyLikes +=1
        companyProfile.save()
@receiver(post_save, sender=Follows)
def increment_company_followers(sender, instance, created, **kwargs):
    if created:
        companyProfile = CompanyProfile.objects.get(pk=instance.company.pk)
        companyProfile.companyFollows +=1
        companyProfile.save()
@receiver(post_save, sender= Reviews)
def increment_company_reviews(sender, instance, created, **kwargs):
     if created:
        companyProfile = CompanyProfile.objects.get(pk=instance.company.pk)
        companyProfile.companyReviews +=1
        companyProfile.save()
@receiver(post_delete, sender=Likes)
def decrement_company_likes(sender, instance, **kwargs):
    companyProfile = CompanyProfile.objects.get(pk=instance.company.pk)
    companyProfile.companyLikes -=1
    companyProfile.save()
@receiver(post_delete, sender=Follows)
def decrement_company_followers(sender, instance, **kwargs):
    companyProfile = CompanyProfile.objects.get(pk=instance.company.pk)
    companyProfile.companyFollows -=1
    companyProfile.save()
    