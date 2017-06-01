from __future__ import absolute_import, unicode_literals
from sum_integers.celery import app
from .models import Data
import json
import numpy as np
from celery import Task, exceptions


# class SafeTask(Task):
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print("lofodfoodfofdool")
#         return {'error': exc}


@app.task
def handle_data(input, data_id):
    def test_func(data):
        json_data = json.loads(data)

        a = []
        b = []

        for x in json_data:
            a.append(x['a'])
            b.append(x['b'])

        a = np.array(a, dtype=np.int)
        b = np.array(b, dtype=np.int)

        res = np.sum(np.multiply(a, b))

        return {'result': str(res)}

    try:
        return test_func(input)
    except Exception as ex:
        data = Data.objects.get(id=data_id)

        data.output = {}
        data.is_success = False
        data.error_message = ex

        data.save()


@app.task
def load_data(data_id):
    dataset = Data.objects.get(id=data_id)

    input_data = getattr(dataset, 'input')

    return input_data


@app.task
def save_result(result, data_id):
    if result is None:
        return

    data = Data.objects.get(id=data_id)

    print("data_id={}, result={}".format(data_id, result))

    data.output = result
    data.is_success = True
    data.error_message = 'no errors'

    data.save()

