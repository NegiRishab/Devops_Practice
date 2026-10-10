output "cluster_name" {
  value = module.my_eks.cluster_name
}

output "ecr_registry" {
  value = split("/", aws_ecr_repository.app["taskboard-backend"].repository_url)[0]
}

output "backend_repository_url" {
  value = aws_ecr_repository.app["taskboard-backend"].repository_url
}

output "frontend_repository_url" {
  value = aws_ecr_repository.app["taskboard-frontend"].repository_url
}
