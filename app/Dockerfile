# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY sample_app.log /var/log/sample_app.log

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]

