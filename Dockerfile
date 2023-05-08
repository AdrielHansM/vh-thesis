# Start from a base image
FROM python:3.11.1-slim

# Set the working directory
WORKDIR /vehicle-detection

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copy the application code into the container
COPY ./app app

# Run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
