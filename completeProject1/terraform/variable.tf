variable "linode_token" {
  description = "Linode API token"
  type        = string
  sensitive   = true
}

variable "linode_region" {
  description = "Linode region"
  type        = string
  default     = "ap-west"
}

variable "linode_type" {
  description = "Linode instance type"
  type        = string
  default     = "g6-nanode-1"
}

variable "linode_image" {
  description = "Linode image"
  type        = string
  default     = "linode/ubuntu24.04"
}

variable "ssh_public_key" {
  description = "SSH public key used to access the server"
  type        = string
}