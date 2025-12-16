# Use an official lightweight Python image
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /code

# Copy requirements from the root context
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the 'project' folder contents into the container's workdir
COPY project /code

# Run the application
# host 0.0.0.0 is required for Docker containers to be accessible
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
