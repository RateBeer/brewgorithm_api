{
  "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecs:DeregisterContainerInstance",
                "ecs:DiscoverPollEndpoint",
                "ecs:Poll",
                "ecs:RegisterContainerInstance",
                "ecs:StartTelemetrySession",
                "ecs:UpdateContainerInstancesState",
                "ecs:Submit*",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "${brewgorithm_read_log_group_arn}",
                "${brewgorithm_write_log_group_arn}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeParameters"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameters"
            ],
            "Resource": [
              "arn:aws:ssm:${aws_region}:${aws_account_id}:parameter${ssm_key_ratebeer_db_user}",
              "arn:aws:ssm:${aws_region}:${aws_account_id}:parameter${ssm_key_ratebeer_db_pass}"
            ]
        },
        {
           "Effect":"Allow",
           "Action":[
              "kms:Decrypt"
           ],
           "Resource":[
              "arn:aws:kms:${aws_region}:${aws_account_id}:alias/aws/ssm"
           ]
        }
    ]
}
