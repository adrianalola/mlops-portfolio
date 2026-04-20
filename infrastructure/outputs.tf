output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.api_server.public_ip
}

output "s3_bucket_name" {
  description = "S3 bucket for model artifacts"
  value       = aws_s3_bucket.model_artifacts.bucket
}

output "api_url" {
  description = "URL to access the API"
  value       = "http://${aws_instance.api_server.public_ip}:8000"
}
