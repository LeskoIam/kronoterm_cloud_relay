# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

COPY ./prod_requirements.txt /app
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r prod_requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src /app/src
COPY ./LICENSE /app
COPY ./README.md /app
COPY ./pyproject.toml /app

# Make port 8555 available to the world outside this container
EXPOSE 8555

# Define environment variables
# ENV_VAR_1=6

# Run app when the container launches
CMD ["fastapi", "run", "src/kronoterm_cloud_relay.py", "--host=0.0.0.0", "--port=8555"]
