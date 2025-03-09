# Use an official Python image as a base
FROM mcr.microsoft.com/devcontainers/python:3.10

# Install any necessary dependencies here
RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /workspace

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Set environment variables based on system type (OS-dependent)
# Here you can set default values for your variables if needed
ARG DOCKER_SOCKET_PATH="/var/run/docker.sock"
ARG WORKSPACE_ENV_FILE="/workspace/.env"

# Expose ports that your app will use
EXPOSE 8000 8501

# Ensure .env file is not copied into the image (handled by bind mount in devcontainer.json)
RUN echo "set -o allexport; [ -f $WORKSPACE_ENV_FILE ] && source $WORKSPACE_ENV_FILE; set +o allexport" >> ~/.bashrc

# Set the entrypoint (adjust as needed for your app)
CMD ["bash"]