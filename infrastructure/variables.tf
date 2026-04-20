variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used for naming resources"
  type        = string
  default     = "mlops-portfolio"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"  # Free tier eligible
}

variable "s3_bucket_name" {
  description = "S3 bucket name for model artifacts (must be globally unique)"
  type        = string
  default     = "mlops-portfolio-models-2026"
}
