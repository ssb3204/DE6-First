from django.db import models

# Create your models here.

class JobPosting(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.title} - {self.company}"