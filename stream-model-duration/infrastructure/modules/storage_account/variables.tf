variable "storage_account_name" {
  type        = string
  description = "The name of the existing Azure Storage Account"
}

variable "container_name" {
  type        = string
  description = "The name of the existing blob container in the storage account"
}

variable "resource_group_name" {
  type        = string
  description = "The resource group containing the storage account"
}
