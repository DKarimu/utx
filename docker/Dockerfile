# Use the official Python image as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONPATH=$PYTHONPATH:/app/brokers
ENV PYTHONPATH=$PYTHONPATH:/app/config
ENV PYTHONPATH=$PYTHONPATH:/app/data
ENV PYTHONPATH=$PYTHONPATH:/app/management
ENV PYTHONPATH=$PYTHONPATH:/app/management/commands
ENV PYTHONPATH=$PYTHONPATH:/app/strategies
ENV PYTHONPATH=$PYTHONPATH:/app/utils
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose the port that the app will run on
EXPOSE 8080

# Run the command to start the Django development server
# CMD ["bash", "torun.sh"]
