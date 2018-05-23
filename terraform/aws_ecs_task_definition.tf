data "template_file" "brewgorithm_read_ecs_task_definition" {
  template = "${file("${path.module}/templates/brewgorithm_read_ecs_task_definition.json.tpl")}"

  vars {
    name                 = "brewgorithm-api-read"
    cpu                  = "${var.container_cpu}"
    memory               = "${var.container_memory}"
    memory_reservation   = "${var.container_memory_reservation}"
    container_port       = 5000
    env_vars             = "[{\"name\": \"WRITE_API\", \"value\": \"0\"} ]"
    log_group            = "Brewgorithm_API_Read_${var.name}" # Feature request to be able to reference the Terraform resource directly.
    log_region           = "${data.aws_region.current.name}"
    image_uri            = "${var.image_uri}"
  }
}

resource "aws_ecs_task_definition" "brewgorithm_read" {
  family = "brewgorithm-api-read"

  # If the *CONTAINER* needs IAM permissions, they will be defined in task_role_arn
  container_definitions = "${data.template_file.brewgorithm_read_ecs_task_definition.rendered}"

  task_role_arn = "${aws_iam_role.brewgorithm.arn}"
}

data "template_file" "brewgorithm_write_ecs_task_definition" {
  template = "${file("${path.module}/templates/brewgorithm_write_ecs_task_definition.json.tpl")}"

  vars {
    name                 = "brewgorithm-api-write"
    cpu                  = "${var.container_cpu}"
    memory               = "${var.container_memory}"
    memory_reservation   = "${var.container_memory_reservation}"
    container_port       = 5000
    env_vars             = "[{\"name\": \"WRITE_API\", \"value\": \"1\"} ]"
    log_group            = "Brewgorithm_API_Write_${var.name}" # Feature request to be able to reference the Terraform resource directly.
    log_region           = "${data.aws_region.current.name}"
    image_uri            = "${var.image_uri}"
  }
}

resource "aws_ecs_task_definition" "brewgorithm_write" {
  family = "brewgorithm-api-write"

  # If the *CONTAINER* needs IAM permissions, they will be defined in task_role_arn
  container_definitions = "${data.template_file.brewgorithm_write_ecs_task_definition.rendered}"

  task_role_arn = "${aws_iam_role.brewgorithm.arn}"
}
