FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Install Pandoc
RUN apt-get update && \
    apt-get install -y pandoc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy function app files
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy function code
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY . /home/site/wwwroot
