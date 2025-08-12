variable "project_id" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "storage_account_name" {
  type = string
}

variable "acr_name" {
  type = string
}

variable "eventhub_namespace" {
  type = string
}

variable "source_eventhub_name" {
  type = string
}

variable "output_eventhub_name" {
  type = string
}

variable "function_app_name" {
  type = string
}

variable "container_name" {
  type    = string
  default = "tfstate"
}
