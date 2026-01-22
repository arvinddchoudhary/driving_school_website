resource "aws_security_group" "drivingschool_sg" {
  name        = "drivingschool_sg"
  description = "Allow SSH, HTTP, Nagios"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5666
    to_port     = 5666
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "app_server" {
  ami             = data.aws_ami.ubuntu.id
  instance_type   = var.instance_type
  key_name        = var.key_name
  security_groups = [aws_security_group.drivingschool_sg.name]
  tags = {
    Name = "DrivingSchool-App"
  }
}

resource "aws_instance" "nagios_server" {
  ami             = data.aws_ami.ubuntu.id
  instance_type   = var.instance_type
  key_name        = var.key_name
  security_groups = [aws_security_group.drivingschool_sg.name]
  tags = {
    Name = "Nagios-Monitor"
  }
}

output "app_ip" {
  value = aws_instance.app_server.public_ip
}

output "nagios_ip" {
  value = aws_instance.nagios_server.public_ip
}
