resource "aws_alb_target_group" "brewgorithm" {
  name = "Brewgorithm-API-${var.name}"

  # This is just the default port that is used when new instances are registered with this target
  # group; really it will end up un-used since the ECS Service will register itself under
  # whatever port it comes up as.
  port     = "5000"

  protocol = "HTTP"
  vpc_id   = "${var.vpc_id}"

  deregistration_delay = "${var.deregistration_delay}"

  health_check {
    path     = "/_health"
    port     = "traffic-port"
    protocol = "HTTP"

    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 20
    timeout             = 15
    matcher             = "200"
  }

  tags {
    Comment = "Managed by Terraform"
  }
}
