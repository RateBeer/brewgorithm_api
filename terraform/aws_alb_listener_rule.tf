resource "aws_alb_listener_rule" "brewgorithm" {
  listener_arn = "${var.alb_listener_arn}"
  priority     = "${var.target_group_priority}"

  action {
    type             = "forward"
    target_group_arn = "${aws_alb_target_group.brewgorithm.arn}"
  }

  condition {
    field  = "host-header"
    values = ["${var.api_host}"]
  }
}

######## TEMPORARY #########
# While we switch from old-Brewgorithm infra; we just want to have an `api.brewgorithm` endpoint to be supported.

resource "aws_alb_listener_rule" "temporary_brewgorithm" {
  listener_arn = "${var.alb_listener_arn}"
  priority     = "${var.target_group_priority + 2}"

  action {
    type             = "forward"
    target_group_arn = "${aws_alb_target_group.brewgorithm.arn}"
  }

  condition {
    field  = "host-header"
    values = ["api.ratebeer.com"]
  }
}

######## TEMPORARY #########
