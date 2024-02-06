# Use the official Python image as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONPATH=$PYTHONPATH:/app/apps/brokers:/app/apps/config:/app/apps/data:/app/apps/strategies:/app/apps/utils:/app/apps/tests \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/

# Copy the rest of the project files into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the entry point for the container
# ENTRYPOINT ["bash", "torun.sh"]

# Expose the port that the app will run on
EXPOSE 8080
