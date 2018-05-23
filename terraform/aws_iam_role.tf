data "aws_iam_policy_document" "ecs_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "brewgorithm" {
  name = "Brewgorithm-${var.name}"
  description = "Terraform - ECS Role for Brewgorithm"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_assume_role_policy.json}"
}
