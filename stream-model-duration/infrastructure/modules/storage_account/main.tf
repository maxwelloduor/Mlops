data "azurerm_storage_account" "this" {
  name                = var.storage_account_name
  resource_group_name = var.resource_group_name
}

data "azurerm_storage_container" "model_container" {
  name                 = var.container_name
  storage_account_name = data.azurerm_storage_account.this.name
}

output "container_name" {
  value = data.azurerm_storage_container.model_container.name
}



