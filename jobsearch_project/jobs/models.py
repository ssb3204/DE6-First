from django.db import models


class JobPosting(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField()
    source = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.company} - {self.title} (출처: {self.source})'