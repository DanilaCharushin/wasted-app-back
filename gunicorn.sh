echo " -- BUILD PROGRESS WILL BE DISPLAYED IN LOGS SECTION -- "

echo " -- [INFO] Run collectstatic..."
python src/manage.py collectstatic --no-input

echo " -- [INFO] Run migrate..."
python src/manage.py migrate

echo " -- [INFO] Starting gunicorn with 2 workers..."
gunicorn src.core.wsgi:application --log-file -