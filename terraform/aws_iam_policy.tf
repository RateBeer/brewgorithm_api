data "template_file" "brewgorithm_access_policy" {
  template = "${file("${path.module}/templates/brewgorithm_access_policy.json.tpl")}"

  vars {
    aws_region                      = "${data.aws_region.current.name}"
    aws_account_id                  = "${data.aws_caller_identity.current.account_id}"
    brewgorithm_read_log_group_arn  = "${aws_cloudwatch_log_group.brewgorithm_read.arn}"
    brewgorithm_write_log_group_arn = "${aws_cloudwatch_log_group.brewgorithm_write.arn}"
  }
}

resource "aws_iam_policy" "brewgorithm" {
  name = "Brewgorithm-${var.name}"
  description = "Terraform - Brewgorithm"

  policy = "${data.template_file.brewgorithm_access_policy.rendered}"
}


