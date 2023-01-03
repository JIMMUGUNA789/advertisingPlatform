from django.db import models
from users.models import CustomUser
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
    operatingHours = models.JSONField()
    

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
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


