
provider "aws" {
 region = "ap-south-1"
}



variable "vpc_cidr_block" {}
variable "private_subnets" {}
variable "public_subnets" {}

data "aws_availability_zones" "available_azs" {}

module "my_vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.6.1"

  name            = "my-vpc"
  cidr            = var.vpc_cidr_block
  azs             = data.aws_availability_zones.available_azs.names
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  tags = {

    "kubernetes.io/cluster/my-cluster" = "shared"

  }

  public_subnet_tags = {

    "kubernetes.io/cluster/my-cluster" = "shared"
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {

    "kubernetes.io/cluster/my-cluster" = "shared"
    "kubernetes.io/role/internal-elb"  = "1"
  }

}
