# Deploy Classification Model pipeline with Terraform using Amazon SageMaker

This repository contains Infrastructure as Code (IaC) to create and manage AWS infrastructure for classification pipeline that predicts loan eligibility of customers with SageMaker and 
Step Functions.

### Deploy AWS Infrastructure with Terraform
In order to deploy the ML pipeline, you will need to adjust the project name variable. The code for the Terraform part is in this repository in the folder:
```shell script
/terraform
```

When initialising for the first time:

Follow the steps below to deploy the infrastructure with Terraform.

```shell script
export AWS_PROFILE=<your_aws_cli_profile_name>

cd terraform/infrastructure

terraform init

terraform plan

terraform apply
```
Check the output and make sure the planned resources appear correctly and confirm with ‘yes’ in the apply stage if
everything is correct. Once successfully applied, go to ECR (or check the output of Terraform in the Terminal) 
and get the URL for your ECR repository just created via Terraform.


### Deploy Docker Image to ECR using GitHub Actions

For the ML pipeline and SageMaker to train and provision an endpoint for inference, you need to provide a Docker image and store it in ECR. 

#### Store AWS credentials in GitHub Secrets
In your GitHub repository, go to Settings > Secrets and add the AWS access key ID and secret access key as secrets. 

#### Set up GitHub Actions workflow
Make sure that the AWS_REGION and ECR_REPOSITORY environment variables in the .github/workflow/aws.yaml file are compatible with the terraform configuration. 
You can also get the ECR repository name through the AWS console.

#### Commit and push changes
Commit the workflow file and any other changes you've made, then push them to your GitHub repository.

#### Monitor the workflow
Go to the "Actions" tab in your GitHub repository to monitor the progress of the workflow. 
If everything is set up correctly, it should build your Docker image and push it to your AWS ECR repository whenever changes are pushed to the specified branch.

#### Check the ECR repository
After the build and deployment process is successful, you can check your ECR repository via the AWS console.
An image tagged with "latest" will be created under the repository.

### Run the ML pipeline

In order to train and run the ML pipeline, go to Step Functions and start the execution. You can check progress of
SageMaker also in the Training Jobs section of SageMaker and once the SageMaker Endpoint is created you can 
also check your SageMaker Endpoint. After running the State Machine in Step Functions successfully, you will see the
SageMaker Endpoint being created in the AWS Console in the SageMaker Endpoints section. Make sure to 
wait for the Status to change to “InService”.

### Invoke your endpoint

In order to invoke your endpoint (in this example for the iris dataset), you can use the following
Python script with boto3 (Python SDK) to invoke your endpoint, for example from a Amazon SageMaker notebook.
```python
import boto3
from io import StringIO
import pandas as pd

client = boto3.client('sagemaker-runtime')

endpoint_name = 'Your endpoint name' # Your endpoint name.
content_type = "text/csv"   # The MIME type of the input data in the request body.

payload = pd.DataFrame([["LP001005", "Female", "Yes", 0, "Graduate", "Yes", 30000, 100, 66.0, 36.0, 1.0, "Urban"]])
csv_file = StringIO()
payload.to_csv(csv_file, sep=",", header=False, index=False)
payload_as_csv = csv_file.getvalue()

response = client.invoke_endpoint(
    EndpointName=endpoint_name, 
    ContentType=content_type,
    Body=payload_as_csv
    )

label = response['Body'].read().decode('utf-8')
print(label)
```

### Cleanup

In order to clean up, you can destroy the infrastructure created by Terraform with the command “terraform destroy”. 
But you will need to delete the data and files in the S3 buckets first. Further, the SageMaker Endpoint (or multiple
SageMaker Endpoints if run multiple times) created via Step Functions is not managed via Terraform, but rather deployed
when running the ML pipeline with Step Functions. Therefore, make sure you delete the SageMaker Endpoints created via
the Step Function ML pipeline as well to avoid unnecessary costs.

### Steps:

- Delete the dataset in the S3 training bucket and all models you trained via the ML pipeline in the S3 bucket for the
 models in the AWS Console or via the AWS CLI
 
- Destroy the infrastructure created via Terraform
```shell script
cd terraform/infrastructure

terraform destroy
```
- Delete the SageMaker Endpoints, Endpoint Configuration and Models created via the Step Function in the AWS Console
or via the AWS CLI.
