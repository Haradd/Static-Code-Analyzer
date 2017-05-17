from django.db import models
from django.utils import timezone



class Report(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return self.name