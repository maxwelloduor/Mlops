data "azurerm_eventhub_namespace" "this" {
  name                = var.namespace_name
  resource_group_name = var.resource_group_name
}

data "azurerm_eventhub" "source" {
  name                = var.source_eventhub_name
  namespace_name      = data.azurerm_eventhub_namespace.this.name
  resource_group_name = var.resource_group_name
}

data "azurerm_eventhub" "output" {
  name                = var.output_eventhub_name
  namespace_name      = data.azurerm_eventhub_namespace.this.name
  resource_group_name = var.resource_group_name
}
