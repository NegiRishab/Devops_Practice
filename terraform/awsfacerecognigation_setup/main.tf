terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.54.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_iam_policy" "face_recognition" {
  name = "student-face-recognition-policy"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "rekognition:DetectFaces",
          "rekognition:IndexFaces",
          "rekognition:SearchFacesByImage",
          "rekognition:DeleteFaces",
          "rekognition:DescribeCollection"
        ]

        Resource = "*"
      }
    ]
  })
}

resource "null_resource" "rekognition_collection" {
  triggers = {
    collection_id = var.collection_id
    region        = var.aws_region
  }

  provisioner "local-exec" {
    command = <<-EOT
      aws rekognition create-collection \
        --collection-id ${var.collection_id} \
        --region ${var.aws_region} \
        || true
    EOT
  }
}