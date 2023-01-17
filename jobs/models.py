from django.db import models
from companies.models import CompanyProfile

# Create your models here.
class Jobs(models.Model):
    JOB_TYPE_CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),


    )
    JOB_LEVEL_CHOICES = (
        ('Entry Level', 'Entry Level'),
        ('Mid Level', 'Mid Level'),
        ('Senior Level', 'Senior Level'),

    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.IntegerField(null=True, blank=True)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    jobType = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Full Time')
    jobLevel = models.CharField(max_length=20, choices=JOB_LEVEL_CHOICES, default='Mid Level')
    applicationDeadline = models.DateField()
    noOfVacancies = models.IntegerField(default=1)
    noOfApplicants = models.IntegerField(default=0)


    # create a choice field for job level
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Jobs'