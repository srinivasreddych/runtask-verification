# runtask-verification
Summary: This is to verify if the RunTask calls have succeeded or not and alert accordingly. For ECS Service events, we could just read them or create appropriate cloudwatch event rules to get triggered upon failure to launch tasks, whereas for Batch Jobs/ECS Scheduled tasks/native RunTask API calls, there is currently no straightforward way to get notifed if there are any issues (for ex: AGENT, No ContainerInstances found etc. 
Note: The solution has SAM template to create CW rule, lambda function, IAM resources.

## Commands to run:

`aws cloudformation package --region us-east-1 --template-file runtask-verification.yaml \
--s3-bucket <<s3_bucket>> \
--output-template-file runtask-verification-transformed.yaml`

`aws cloudformation deploy --template-file /home/ec2-user/environment/runtask-verification-transformed.yml --stack-name runtask-verification --parameter-overrides NameOfSolution='runtask-verification' --capabilities CAPABILITY_NAMED_IAM`

Note:
1) Replace s3_bucket with the desired s3 bucket in the format bucket-test (do not use 's3://' syntax)

