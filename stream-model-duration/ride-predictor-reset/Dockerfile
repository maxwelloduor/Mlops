FROM mcr.microsoft.com/azure-functions/python:4-python3.10


ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY . /home/site/wwwroot
RUN pip install -r /home/site/wwwroot/requirements.txt
