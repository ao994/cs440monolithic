# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5002
# Set the environment variable for Flask to run in production
ENV FLASK_ENV=production

# Define the command to run the Flask application
CMD ["python", "review_service.py"]