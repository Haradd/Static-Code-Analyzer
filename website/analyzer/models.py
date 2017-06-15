from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils import timezone



class Report(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return self.user.username + ' - ' + self.name