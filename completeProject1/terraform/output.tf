output "server_ip" {
  description = "Public IPv4 address of the application server"
  value       = tolist(linode_instance.app_server.ipv4)[0]
}