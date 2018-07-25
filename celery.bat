@echo off
del C:\wwwroot\easywork\celerybeat.pid
start cmd /k "python manage.py celery beat"
start cmd /k "python manage.py celery worker -l info"