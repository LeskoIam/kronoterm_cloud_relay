# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app/src

COPY ./pyproject.toml /app
COPY ./requirements.txt /app
COPY ./dev_requirements.txt /app
COPY ./prod_requirements.txt /app
COPY ./LICENSE /app
COPY ./README.md /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pyopenssl
# Make port 8555 available to the world outside this container
EXPOSE 8555

# Define environment variable
ENV FLASK_APP=src/kronoterm_cloud_relay.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8555", "--cert=adhoc"]
