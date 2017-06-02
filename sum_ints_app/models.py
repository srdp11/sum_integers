from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.aggregates import Max

# Create your models here.


class Data(models.Model):
    input = JSONField()

    def __str__(self):
        return "id={}".format(self.id)


class ResultManager(models.Manager):
    def last_result(self):
        data_count = Data.objects.count()
        result_count = self.count()

        if data_count == 0 or result_count == 0:
            return self.none()

        result_data = self.all().order_by('id')

        if result_count % data_count != 0:
            result_data = result_data[:(result_data.count() - (result_count % data_count))]

        return result_data.order_by('id')[:data_count]
        # # for id in ids:
        # #     obj = self.get(id=id).aggregate(Max('created_at'))
        # #     result_data = result_data | obj
        #
        #
        #
        # return result_data


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

    def __str__(self):
        return "id={}, run={}, input={}, output={}, is_success={}, error={}".format(self.id,
                                                                                    self.run,
                                                                                    self.input,
                                                                                    self.output,
                                                                                    self.is_success,
                                                                                    self.error_message)

