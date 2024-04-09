project_name = "ml-pipeline" 
region = "eu-north-1"

training_instance_type = "ml.m5.xlarge"
inference_instance_type = "ml.m5.xlarge"
volume_size_sagemaker = 5

handler_path  = "../../src/lambda_function"
handler       = "config_lambda.lambda_handler"