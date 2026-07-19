provider "aws" {
  region = "ap-south-1"
  
  
}

resource "aws_vpc" "my_vpc" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name: "${var.env_prefix}-vpc"
  }
}

module "my-app-subnet" {
  source = "./modules/subnet"
  vpc_id = aws_vpc.my_vpc.id
  default_route_table_id = aws_vpc.my_vpc.default_route_table_id
  subnet_cidr_block = var.subnet_cidr_block
  availability_zone = var.availability_zone
  env_prefix = var.env_prefix
  vpc_cidr_block = var.vpc_cidr_block
}


module "my-webserver" {
  source = "./modules/webserver"
  vpc_cidr_block = var.vpc_cidr_block
  subnet_cidr_block = var.subnet_cidr_block
  availability_zone = var.availability_zone
  env_prefix = var.env_prefix
  my_ip = var.my_ip
  instance_type = var.instance_type
  public_key_path = var.public_key_path
  vpc_id = aws_vpc.my_vpc.id
  subnet_id = module.my-app-subnet.subnet.id

}