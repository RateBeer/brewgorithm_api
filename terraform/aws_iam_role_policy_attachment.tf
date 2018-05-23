resource "aws_iam_role_policy_attachment" "brewgorithm" {
  role       = "${aws_iam_role.brewgorithm.name}"
  policy_arn = "${aws_iam_policy.brewgorithm.arn}"
}
