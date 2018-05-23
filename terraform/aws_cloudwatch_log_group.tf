resource "aws_cloudwatch_log_group" "brewgorithm_read" {
  name = "Brewgorithm_API_Read_${var.name}"

  tags {
    Name    = "${var.name}"
    Comment = "Managed by Terraform"
  }
}

resource "aws_cloudwatch_log_group" "brewgorithm_write" {
  name = "Brewgorithm_API_Write_${var.name}"

  tags {
    Name    = "${var.name}"
    Comment = "Managed by Terraform"
  }
}
