#!/bin/bash

# Default tag is 'latest'
TAG=${1:-latest}

echo "Building Docker image: csv-to-qif:$TAG"

# Build the Docker image
docker build -t "csv-to-qif:$TAG" .

if [ $? -eq 0 ]; then
    echo "--------------------------------------------------"
    echo "Successfully built: csv-to-qif:$TAG"
    echo "--------------------------------------------------"
else
    echo "--------------------------------------------------"
    echo "Error: Docker build failed."
    echo "--------------------------------------------------"
    exit 1
fi
