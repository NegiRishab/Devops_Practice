output "aws_region" {
  description = "AWS region used for Rekognition"
  value       = var.aws_region
}

output "rekognition_collection_id" {
  description = "Rekognition face collection ID"
  value       = var.collection_id
}

output "face_recognition_policy_arn" {
  description = "IAM policy ARN for face recognition"
  value       = aws_iam_policy.face_recognition.arn
}