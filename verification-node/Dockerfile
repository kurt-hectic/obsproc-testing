# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Update the package list and install mosquitto-clients, jq, and wget
RUN apt-get update && \
    apt-get install -y mosquitto-clients jq wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Default command
CMD ["bash"]