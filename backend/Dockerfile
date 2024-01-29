# Use the official CUDA base image with Python 3.10
FROM nvidia/cuda:12.2.2-base-ubuntu22.04

# Set the working directory
WORKDIR /backend

# Update the package list
RUN apt-get update

# Install Python and pip
RUN apt-get install -y python3.10 python3.10-dev python3-pip

# Install Nvidia container toolkit
# RUN apt-get install -y --no-install-recommends nvidia-container-toolkit

# Copy the requirements file
COPY backend/requirements.txt .

# Install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Copy the rest of the application code
COPY backend .

# Expose the port
EXPOSE 5000

# Set the entry point
CMD ["python", "api.py"]
