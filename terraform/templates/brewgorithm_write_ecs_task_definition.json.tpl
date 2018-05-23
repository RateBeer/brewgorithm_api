[
  {
    "memory": ${memory},
    "portMappings": [
      {
        "hostPort": 0,
        "containerPort": ${container_port},
        "protocol": "tcp"
      }
    ],
    "essential": true,
    "name": "${name}",
    "environment": ${env_vars},
    "image": "${image_uri}:latest",
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${log_group}",
        "awslogs-region": "${log_region}"
      }
    },
    "cpu": ${cpu},
    "memoryReservation": ${memory_reservation}
  }
]
