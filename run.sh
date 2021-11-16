lsof -t -i tcp:8002 | xargs kill -9
export DJANGO_SETTINGS_MODULE=featuringeg_report.settings.base
python manage.py runserver 0.0.0.0:8002
