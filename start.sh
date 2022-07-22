python3 manage.py collectstatic --no-input
python3 manage.py migrate --no-input
python3 manage.py loaddata test_data.json
python3 manage.py runserver 0.0.0.0:8000