# Python version
FROM python:3.11-slim

# Our dir
WORKDIR /app

# Container
COPY . /app

# Installing dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py migrate
# Static files
RUN python manage.py collectstatic --noinput

# Our port
EXPOSE 8000

# Development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
