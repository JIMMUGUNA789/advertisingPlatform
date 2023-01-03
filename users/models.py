from django.db import models

from django.contrib.auth.models import AbstractUser

#create user model
class CustomUser(AbstractUser):
    VISITOR =1
    COMPANYADMIN =2
    ADMIN =3
    ROLE_CHOICES = (
        (VISITOR, 'Visitor'),
        (COMPANYADMIN, 'Company Admin'),
        (ADMIN, 'Admin'),
    )
    phoneNumber = models.CharField(max_length=15)
    profilePicture = models.ImageField(upload_to='images/', blank=True)
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=VISITOR, blank=True, null=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = 'Custom Users'




