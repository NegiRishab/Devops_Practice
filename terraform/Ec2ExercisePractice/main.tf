provider "aws" {
  region = "ap-south-1"


}

variable "env" {}
variable "vpc_cidr" {}
variable "subnet_cidr_block" {}
variable "availibilty_zone" {}
variable "instance_type" {}
variable "key_pair" {}

resource "aws_vpc" "my-vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true

  tags = {
    Name: "${var.env}-vpc"
  }
  
}

resource "aws_subnet" "my-subnet" {
  vpc_id = aws_vpc.my-vpc.id
  cidr_block = var.subnet_cidr_block
  availability_zone = var.availibilty_zone

  tags = {
    Name:"${var.env}-subnet"
  }
}

resource "aws_internet_gateway" "internet-gateway" {
  vpc_id = aws_vpc.my-vpc.id

  tags = {
    Name:"${var.env}-internet-gateway"
  }
  
}

resource "aws_route_table" "my-route-table" {
  vpc_id = aws_vpc.my-vpc.id

 route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet-gateway.id
 }

 tags = {
   Name: "${var.env}-route-table"
 }

  
}

resource "aws_route_table_association" "association" {
  subnet_id = aws_subnet.my-subnet.id
  route_table_id = aws_route_table.my-route-table.id
  
}

resource "aws_security_group" "security-group" {
  name = "${var.env}-security-group"
  description= "Allow Ssh and http and https"
  vpc_id = aws_vpc.my-vpc.id

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
          cidr_blocks = ["0.0.0.0/0"]
    }
  

  tags = {
    Name="${var.env}-security-group"
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

resource "aws_key_pair" "my-pair" {
  key_name = "${var.env}-key-pair"
  public_key = file(var.key_pair)
  
}

resource "aws_instance" "my-instance-1" {
  
  ami = data.aws_ami.latest_aws_image.id
  instance_type = var.instance_type
  subnet_id = aws_subnet.my-subnet.id
  vpc_security_group_ids = [aws_security_group.security-group.id]

  associate_public_ip_address = true
  key_name = aws_key_pair.my-pair.key_name

    tags = {
        Name = "${var.env}-instance-1"
    }

}

resource "aws_instance" "my-instance-2" {
  
  ami = data.aws_ami.latest_aws_image.id
  instance_type = var.instance_type
  subnet_id = aws_subnet.my-subnet.id
  vpc_security_group_ids = [aws_security_group.security-group.id]

  associate_public_ip_address = true
  key_name = aws_key_pair.my-pair.key_name

    tags = {
        Name = "${var.env}-instance-2"
    }

}

resource "aws_instance" "my-instance-3" {
  
  ami = data.aws_ami.latest_aws_image.id
  instance_type = "t3.small"
  subnet_id = aws_subnet.my-subnet.id
  vpc_security_group_ids = [aws_security_group.security-group.id]

  associate_public_ip_address = true
  key_name = aws_key_pair.my-pair.key_name

    tags = {
        Name = "${var.env}-instance-3"
    }

}

output "instance-1_public_ip" {
  value = aws_instance.my-instance-1.public_ip
  
}

output "instance-2_public_ip" {
  value = aws_instance.my-instance-2.public_ip
  
}
output "instance-3_public_ip" {
  value = aws_instance.my-instance-3.public_ip
}