FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . /app/

# Run migrations, collect static files, and start Gunicorn
CMD python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000