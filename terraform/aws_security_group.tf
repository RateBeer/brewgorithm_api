resource "aws_security_group" "brewgorithm" {
  name        = "Brewgorithm-${var.name}"
  description = "Managed by Terraform"
  vpc_id      = "${var.vpc_id}"

  tags {
    Name = "Brewgorithm-${var.name}"
  }
}
