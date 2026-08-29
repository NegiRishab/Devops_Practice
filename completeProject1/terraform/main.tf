resource "linode_instance" "app_server" {

  label = "complete-project1-server"

  region = var.linode_region

  type = var.linode_type

  image = var.linode_image

   authorized_keys = [
    var.ssh_public_key
  ]
}