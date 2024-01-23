# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Update and upgrade system packages
RUN apk update && apk upgrade

# Add a non root user
RUN adduser -D appuser

# Set the working directory in the container
WORKDIR /app

# Set
RUN chown -R appuser:appuser /app

# Upgrade Pip
RUN pip install --upgrade pip

# Install gunicorn
RUN pip install gunicorn

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Switch user
USER appuser

# Set restrictive file permissions
RUN chmod 500 /app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV FLASK_CONFIG production

# Define the command to run your application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]