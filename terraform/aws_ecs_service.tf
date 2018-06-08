resource "aws_ecs_service" "brewgorithm" {
  name            = "brewgorithm-api"
  cluster         = "${var.ecs_cluster_id}"
  task_definition = "${aws_ecs_task_definition.brewgorithm.arn}"
  desired_count   = "${var.number_of_tasks}"

  # The IAM role is required when working with a load balancer so that the service can
  # register itself!
  iam_role = "${var.ecs_service_iam_role_arn}"
  load_balancer {
    target_group_arn = "${aws_alb_target_group.brewgorithm.arn}"
    container_name = "brewgorithm-api"
    container_port = 5000
  }

  health_check_grace_period_seconds = "${var.health_check_grace_period_seconds}"

  deployment_maximum_percent         = "${var.deployment_maximum_percent}"
  deployment_minimum_healthy_percent = "${var.deployment_minimum_healthy_percent}"

  # An ECS service cannot attach itself to a target group that has no load balancer
  # attached to it. Without this; we'll always fail the first-run.
  depends_on = [ "aws_alb_listener_rule.brewgorithm", "aws_ecs_task_definition.brewgorithm" ]

  # While not ideal as this will make it difficult to make changes to the task definition;
  # this will ensure that Terraform doesn't complain when we've bumped the task definition
  # revision via Continuous Integration
  #
  # If we want to change the task definition; we'll then need a deployment or update the service manually
  # to the new task definition.
  #
  # If this is not done - then if we are updating the service to a new revision via CI/CD, then next time
  # we run Terraform, it will try to set the service back down to the task revision it created.
  lifecycle {
    create_before_destroy = true
    ignore_changes        = ["task_definition"]
  }
}

