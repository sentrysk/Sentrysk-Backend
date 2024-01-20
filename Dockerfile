# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV FLASK_CONFIG production

# Set the working directory in the container
WORKDIR /app

# Install gunicorn
RUN pip install gunicorn

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define the command to run your application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]