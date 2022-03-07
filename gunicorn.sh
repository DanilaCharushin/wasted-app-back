echo " -- BUILD PROGRESS WILL BE DISPLAYED IN LOGS SECTION -- "

echo " -- [INFO] Run collectstatic..."
python manage.py collectstatic --no-input

echo " -- [INFO] Run migrate..."
python manage.py migrate

echo " -- [INFO] Starting gunicorn with 2 workers..."
gunicorn config.wsgi:application --log-file -