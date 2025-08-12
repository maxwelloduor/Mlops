output "source_eventhub_name" {
  value = data.azurerm_eventhub.source.name
}

output "output_eventhub_name" {
  value = data.azurerm_eventhub.output.name
}

output "namespace_name" {
  value = data.azurerm_eventhub_namespace.this.name
}
