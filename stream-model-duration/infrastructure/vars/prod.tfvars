project_id             = "mlops-zoomcamp"
resource_group_name    = "stream-model-duration-prod-rg"
location               = "East US"

acr_name               = "prodstreammodelduration"
storage_account_name   = "prodmlflowmodels"
eventhub_namespace     = "stream-mlops-ns" # replace with actual namespace
source_eventhub_name   = "prod-ride-input"
output_eventhub_name   = "prod-ride-predictions"

function_app_name      = "ride-predictor-fn"
