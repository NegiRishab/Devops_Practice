provider "aws" {
  region = "ap-south-1"
}

variable "cider_blocks" {
  description = "CIDR blocks for the development"
  type = list(object({
    cider_block = string
    name = string
  }))
 
}
variable "av_zone" {}
resource "aws_vpc" "develoment_vpc" {
  cidr_block = var.cider_blocks[0].cider_block

    tags = {
        Name = var.cider_blocks[0].name
        vpc_env = "development"
    }
  
}

resource "aws_subnet" "development_subnet" {
  vpc_id = aws_vpc.develoment_vpc.id
  cidr_block = var.cider_blocks[1].cider_block
  availability_zone = var.av_zone

  tags = {
     Name = var.cider_blocks[1].name
  }
}

