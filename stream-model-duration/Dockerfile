FROM mcr.microsoft.com/azure-functions/python:4-python3.10


ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Install build tools and BLAS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/site/wwwroot

# Copy only requirements.txt first to leverage Docker caching
COPY requirements.txt .

# Install Cython and dependencies with no-build-isolation to use prebuilt wheels
RUN pip install --no-build-isolation Cython==0.29.36
RUN pip install --no-build-isolation -r requirements.txt

# Copy the rest of the application
COPY ride-predictor-reset/ /home/site/wwwroot/
COPY . .

# Ensure pip is up-to-date (optional, but recommended)
RUN pip install --upgrade pip