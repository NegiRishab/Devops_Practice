provider "aws" {
  region = "ap-south-1"
}

variable vpc_cidr_block {}
variable subnet_cidr_block {}
variable availability_zone {}
variable env_prefix {}
variable my_ip {}
variable instance_type {}
variable public_key_path {}
  
  


resource "aws_vpc" "my_vpc" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name: "${var.env_prefix}-vpc"
  }
}

resource "aws_subnet" "my_subnet" {
  vpc_id = aws_vpc.my_vpc.id
  cidr_block = var.subnet_cidr_block
  availability_zone = var.availability_zone
  tags = {
    Name: "${var.env_prefix}-subnet"
  }
}

resource "aws_internet_gateway" "my_internet_gateway" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    Name: "${var.env_prefix}-internet-gateway"
  }
}

# resource "aws_route_table" "my_route_table" {
#   vpc_id = aws_vpc.my_vpc.id
#   route {
#     cidr_block = "0.0.0.0/0"
#     gateway_id = aws_internet_gateway.my_internet_gateway.id
#   }
#   tags = {
#     Name: "${var.env_prefix}-route-table"
#   }
  
# }

# resource "aws_route_table_association" "my_route_table_association" {
#   subnet_id = aws_subnet.my_subnet.id
#   route_table_id = aws_route_table.my_route_table.id
  
# }

resource "aws_default_route_table" "main_route_table" {
  default_route_table_id = aws_vpc.my_vpc.default_route_table_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_internet_gateway.id
  }
  tags = {
    Name = "${var.env_prefix}-default-route-table"
  }
}

# resource "aws_security_group" "my_security_group" {
#   name = "${var.env_prefix}-security-group"
#   vpc_id = aws_vpc.my_vpc.id
#   description = "Security group for ${var.env_prefix} environment"

#   ingress {
#     from_port = 22
#     to_port = 22
#     protocol = "tcp"
#     cidr_blocks = [var.my_ip]
#   }
#   ingress {
#     from_port = 8080
#     to_port = 8080
#     protocol = "tcp"
#     cidr_blocks = [var.my_ip]
#   }
#   egress {
#     from_port = 0
#     to_port = 0
#     protocol = "-1"
#     cidr_blocks = [var.my_ip]
#     prefix_list_ids = []
#   }

#   tags = {
#     Name = "${var.env_prefix}-security-group"
#   }
# }

resource "aws_default_security_group" "default_security_group" {
  vpc_id = aws_vpc.my_vpc.id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [var.my_ip]
  }
  ingress {
    from_port = 8080
    to_port = 8080
    protocol = "tcp"
    cidr_blocks = [var.my_ip]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [var.my_ip]
    prefix_list_ids = []
  }

  tags = {
    Name = "${var.env_prefix}-security-group"
  }
}

data "aws_ami" "latest_aws_image" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
  name   = "virtualization-type"
  values = ["hvm"]
}
}


resource "aws_key_pair" "my_key_pair" {
  key_name   = "custom-key-pair"  
  public_key = file(var.public_key_path)  
  
}


resource "aws_instance" "my_ec2_instance" {
  ami = data.aws_ami.latest_aws_image.id
  instance_type = var.instance_type
  associate_public_ip_address = true
  key_name = aws_key_pair.my_key_pair.key_name
  subnet_id = aws_subnet.my_subnet.id
  vpc_security_group_ids = [aws_default_security_group.default_security_group.id]
  availability_zone = var.availability_zone
  tags = {
    Name = "${var.env_prefix}-ec2-instance"
  }
  
}