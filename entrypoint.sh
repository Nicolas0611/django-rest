# entrypoint.sh

# Wait for PostgreSQL to be ready (optional but useful in some cases)
# You can install `wait-for-it` or a similar script to wait for DB readiness
# ./wait-for-it.sh db:5432 -- python manage.py migrate

# Run migrations
python manage.py migrate

# Start Django application
python manage.py runserver