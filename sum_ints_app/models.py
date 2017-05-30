from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Data(models.Model):
    input = JSONField()
    output = JSONField()
    is_success = models.BooleanField(default=False)
    error_message = models.TextField(default='not-calculated')
