from __future__ import absolute_import, unicode_literals
from sum_integers.celery import app
from .models import Data, Result, Run
import json
import numpy as np


@app.task
def handle_data(input, data_id, run_id):
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
        Result.objects.create(run=Run.objects.get(id=run_id),
                              input=Data.objects.get(id=data_id),
                              output={},
                              is_success=False,
                              error_message=ex)


@app.task
def load_data(data_id):
    dataset = Data.objects.get(id=data_id)

    input_data = getattr(dataset, 'input')

    return input_data


@app.task
def save_result(result, data_id, run_id):
    if result is None:
        return

    Result.objects.create(run=Run.objects.get(id=run_id),
                          input=Data.objects.get(id=data_id),
                          output=result,
                          is_success=True)

    print("data_id={}, result={}".format(data_id, result))

