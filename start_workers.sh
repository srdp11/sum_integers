#!/usr/bin/env bash

celery multi start -A sum_integers load -Q task_load
celery multi start -A sum_integers handle -Q task_handle
celery multi start -A sum_integers save -Q task_save