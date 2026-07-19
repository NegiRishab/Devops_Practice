resource "aws_default_security_group" "default_security_group" {
  vpc_id = var.vpc_id

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
  subnet_id = var.subnet_id
  vpc_security_group_ids = [aws_default_security_group.default_security_group.id]
  availability_zone = var.availability_zone
  tags = {
    Name = "${var.env_prefix}-ec2-instance"
  }
  
}