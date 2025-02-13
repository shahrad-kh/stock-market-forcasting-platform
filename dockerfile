# Use Python 3.11 official image as the base
FROM python:3.11-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    libodbc1 \
    supervisor\
    && rm -rf /var/lib/apt/lists/*

#Set Timezone
ENV TZ=Asia/Tehran
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Install Microsoft ODBC driver
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/ubuntu/20.04/prod focal main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean

# Verify installation of ODBC driver
RUN odbcinst -q -d

# Copy the Supervisor config file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy the requirements file and install dependencies
COPY requirements.linux.txt /app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.linux.txt

# Copy the Django project files
COPY . /app/

# Expose the application port
EXPOSE 8000

# Run migrations and start Gunicorn
ENTRYPOINT ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
