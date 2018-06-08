variable "name" {
  type = "string"

  description = "This will be added to the name of most resources to keep them unique."
}

variable "vpc_id" {
  type = "string"

  description = "ID of the VPC to deploy into."
}

variable "deregistration_delay" {
  default = 60

  description = "Delay for target group deregistration."
}

variable "health_check_grace_period_seconds" {
  default = 120

  description = "Health check grace period for load balancer."
}

variable "deployment_maximum_percent" {
  type = "string"

  default = 200 # The AWS Default
}

variable "deployment_minimum_healthy_percent" {
  type = "string"

  default = 100 # The AWS Default
}

variable "ssm_aws_region" {}
variable "ssm_key_ratebeer_db_user" {}
variable "ssm_key_ratebeer_db_pass" {}

variable "api_host" {}

variable "image_uri" {}
variable "number_of_tasks" {}
variable "ecs_cluster_id" {}
variable "alb_listener_arn" {}
variable "target_group_priority" {}
variable "container_cpu" {}
variable "container_memory" {}
variable "container_memory_reservation" {}
variable "ecs_service_iam_role_arn" {}

