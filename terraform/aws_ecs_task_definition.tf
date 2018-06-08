data "template_file" "brewgorithm_read_ecs_task_definition" {
  template = "${file("${path.module}/templates/brewgorithm_read_ecs_task_definition.json.tpl")}"

  vars {
    name                 = "brewgorithm-api-read"
    cpu                  = "${var.container_cpu}"
    memory               = "${var.container_memory}"
    memory_reservation   = "${var.container_memory_reservation}"
    container_port       = 5000
    env_vars             = "[{\"name\": \"WRITE_API\", \"value\": \"0\"}, {\"name\": \"RATEBEER_DB_HOST\", \"value\": \"db.r8.beer\"}, {\"name\": \"RATEBEER_DB_DATABASE\", \"value\": \"Ratebeer2\"}, {\"name\": \"RATEBEER_DB_PORT\", \"value\": \"1433\"}, {\"name\": \"S3_PATH\", \"value\": \"17-11-20/\"}, {\"name\": \"S3_BUCKET\", \"value\": \"brewgorithm-model\"}, {\"name\": \"SSM_AWS_REGION\", \"value\": \"${var.ssm_aws_region}\"}, {\"name\": \"S3_AWS_REGION\", \"value\": \"${var.s3_aws_region}\"} ]"
    log_group            = "${aws_cloudwatch_log_group.brewgorithm_read.name}"
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
    env_vars             = "[{\"name\": \"WRITE_API\", \"value\": \"1\"}, {\"name\": \"RATEBEER_DB_HOST\", \"value\": \"db.r8.beer\"}, {\"name\": \"RATEBEER_DB_DATABASE\", \"value\": \"Ratebeer2\"}, {\"name\": \"RATEBEER_DB_PORT\", \"value\": \"1433\"}, {\"name\": \"S3_PATH\", \"value\": \"17-11-20/\"}, {\"name\": \"S3_BUCKET\", \"value\": \"brewgorithm-model\"}, {\"name\": \"SSM_AWS_REGION\", \"value\": \"${var.ssm_aws_region}\"}, {\"name\": \"S3_AWS_REGION\", \"value\": \"${var.s3_aws_region}\"} ]"
    log_group            = "${aws_cloudwatch_log_group.brewgorithm_write.name}"
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
