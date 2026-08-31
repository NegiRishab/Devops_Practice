variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "collection_id" {
  description = "AWS Rekognition face collection ID"
  type        = string
  default     = "student-face-collection"
}