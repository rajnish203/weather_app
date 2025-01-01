# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-w", "2", "-b", ":8080", "main:app"]
