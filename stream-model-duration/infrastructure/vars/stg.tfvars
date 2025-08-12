project_id             = "mlops-zoomcamp"
resource_group_name    = "mlflow-rg"
location               = "East US"

acr_name               = "mlregistrynairobi"
storage_account_name   = "mlmodelsstore"
eventhub_namespace     = "rideeventsns" # replace with actual namespace
source_eventhub_name   = "ride-input"
output_eventhub_name   = "ride-predictions"
container_name          = "tfstate"


function_app_name      = "ride-predictor-fn"
