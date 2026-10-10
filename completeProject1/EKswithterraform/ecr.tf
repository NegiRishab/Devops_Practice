resource "aws_ecr_repository" "app" {
  for_each = toset(["taskboard-backend", "taskboard-frontend"])

  name                 = each.value
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
