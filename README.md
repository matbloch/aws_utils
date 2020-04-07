# AWS Utils









## Configuring IAM Policies

> The privileges of the user that will be integrated in production should be limited to a minimum

**Sending Metric Data**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData"
            ],
            "Resource": "*"
        }
    ]
}
```

## IAM Roles for Tasks



