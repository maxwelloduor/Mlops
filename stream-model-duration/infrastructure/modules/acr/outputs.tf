output "login_server" {
  value = data.azurerm_container_registry.acr.login_server
}

output "registry_name" {
  value = data.azurerm_container_registry.acr.name
}

output "registry_id" {
  value = data.azurerm_container_registry.acr.id
}
