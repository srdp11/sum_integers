from django.db import models
from django.contrib.postgres.fields import JSONField
import json

# Create your models here.


class Data(models.Model):
    input = JSONField()

    def __str__(self):
        return "{}".format(self.input)

    def __iter__(self):
        replaced_json = json.loads(self.input)

        return iter([
            ('input', replaced_json)
        ])


class Run(models.Model):
    pass

    def __str__(self):
        return "<id={}>".format(self.id)


class Result(models.Model):
    run = models.ForeignKey(Run)
    input = models.ForeignKey(Data)
    output = JSONField()
    is_success = models.NullBooleanField()
    error_message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __iter__(self):
        return iter([
            ('input', dict(self.input)),
            ('output', self.output),
            ('is_success', self.is_success),
            ('error_message', self.error_message)
        ])

    def __str__(self):
        return "id={}, run={}, input={}, output={}, is_success={}, error={}".format(self.id,
                                                                                    self.run,
                                                                                    self.input,
                                                                                    self.output,
                                                                                    self.is_success,
                                                                                    self.error_message)

