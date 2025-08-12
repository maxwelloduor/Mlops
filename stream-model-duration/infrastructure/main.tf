terraform {
  required_version = ">= 1.0"

  backend "azurerm" {
    resource_group_name  = "mlflow-rg"
    storage_account_name = "mlmodelsstore"
    container_name       = "tfstate"
    key                  = "stream-model-duration.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "acr" {
  source              = "./modules/acr"
  acr_name            = var.acr_name
  resource_group_name = var.resource_group_name
}

module "eventhub" {
  source                = "./modules/eventhub"
  resource_group_name   = var.resource_group_name
  namespace_name        = var.eventhub_namespace
  source_eventhub_name  = var.source_eventhub_name
  output_eventhub_name  = var.output_eventhub_name
}

module "function_app" {
  source              = "./modules/function_app"
  function_app_name   = var.function_app_name
  resource_group_name = var.resource_group_name
}

module "storage_account" {
  source                = "./modules/storage_account"
  container_name        = "tfstate"
  storage_account_name  = var.storage_account_name
  resource_group_name   = var.resource_group_name
}

output "acr_login_server" {
  value = module.acr.login_server
}

output "eventhub_namespace" {
  value = module.eventhub.namespace_name
}

output "function_app_name" {
  value = module.function_app.function_app_name
}

output "storage_blob_endpoint" {
  value = module.storage_account.primary_blob_endpoint
}
