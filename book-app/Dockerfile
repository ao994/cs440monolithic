FROM python:3.9-slim


WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose port 5000 for the web server
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]