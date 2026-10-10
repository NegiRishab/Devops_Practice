terraform {
  required_version = ">= 1.10.0"

  # Supply bucket/key/region using Jenkins' taskboard_tf_backend file.
  backend "s3" {}

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.55.0"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

provider "aws" {
  region = var.aws_region
}
