from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Data(models.Model):
    input = JSONField()


class Result(models.Model):
    input = models.ForeignKey(Data)
    output = JSONField()
    is_success = models.NullBooleanField()
    error_message = models.TextField(null=True)

    def __str__(self):
        return "input={}, output={}, is_success={}, error={}".format(self.input,
                                                                     self.output,
                                                                     self.is_success,
                                                                     self.error_message)
