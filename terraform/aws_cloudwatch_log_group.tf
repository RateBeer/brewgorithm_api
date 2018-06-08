resource "aws_cloudwatch_log_group" "brewgorithm" {
  name = "Brewgorithm_API_${var.name}"

  tags {
    Name    = "${var.name}"
    Comment = "Managed by Terraform"
  }
}
