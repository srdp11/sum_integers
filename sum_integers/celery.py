from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Queue, Exchange

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sum_integers.settings')

app = Celery('sum_integers',
             broker='pyamqp://guest@localhost//',
             backend='amqp://')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('task_load', Exchange('task_load'), routing_key='task_load'),
    Queue('task_handle', Exchange('task_handle'), routing_key='task_handle'),
    Queue('task_save', Exchange('task_save'), routing_key='task_save'),
)

app.conf.task_routes = {
    'sum_ints_app.tasks.load_data': {'queue': 'task_load', 'exchange': 'task_load', 'routing_key': 'task_load'},
    'sum_ints_app.tasks.test_func': {'queue': 'task_handle', 'exchange': 'task_handle', 'routing_key': 'task_handle'},
    'sum_ints_app.tasks.save_result': {'queue': 'task_save', 'exchange': 'task_save', 'routing_key': 'task_save'},
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

if __name__ == '__main__':
    app.start()
