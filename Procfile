web: python manage.py makemigrations && python manage.py migrate &&
 python manage.py collectstatic --noinput &&
 gunicorn ppm_event_manager_django_project.wsgi --log-file -