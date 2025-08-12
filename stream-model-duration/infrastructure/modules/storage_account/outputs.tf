output "storage_account_name" {
  value = data.azurerm_storage_account.this.name
}

output "model_container_name" {
  value = data.azurerm_storage_container.model_container.name
}

output "primary_blob_endpoint" {
  value = data.azurerm_storage_account.this.primary_blob_endpoint
}
