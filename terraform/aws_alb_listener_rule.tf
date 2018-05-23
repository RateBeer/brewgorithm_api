resource "aws_alb_listener_rule" "brewgorithm_read" {
  listener_arn = "${var.alb_listener_arn}"
  priority     = "${var.target_group_priority}"

  action {
    type             = "forward"
    target_group_arn = "${aws_alb_target_group.brewgorithm_read.arn}"
  }

  condition {
    field  = "host-header"
    values = ["${var.target_group_host_pattern}"]
  }

  condition {
    field  = "path-pattern"
    values = ["/model"]
  }
}

resource "aws_alb_listener_rule" "brewgorithm_write" {
  listener_arn = "${var.alb_listener_arn}"
  priority     = "${var.target_group_priority + 1}"

  action {
    type             = "forward"
    target_group_arn = "${aws_alb_target_group.brewgorithm_write.arn}"
  }

  condition {
    field  = "host-header"
    values = ["${var.target_group_host_pattern}"]
  }

  condition {
    field  = "path-pattern"
    values = ["/write-model"]
  }
}