FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for pdfplumber
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir pdfplumber

# Copy the application code
COPY src/ /app/src/
# Add src to PYTHONPATH so imports like 'from common import ...' work
ENV PYTHONPATH="/app/src"

# Create the necessary directories in the container
# We'll rely on volume mounting for input/output, but we ensure they exist
RUN mkdir -p input output

# We'll use a wrapper or just allow the user to specify the script.
# To make it easy, we'll set the entrypoint to python, and the user can pass the script name and args.
ENTRYPOINT ["python"]
