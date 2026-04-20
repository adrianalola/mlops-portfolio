#!/bin/bash
# Este script corre automáticamente cuando EC2 arranca por primera vez

# Instalar Docker
yum update -y
yum install -y docker
systemctl start docker
systemctl enable docker

# Variables de entorno
export S3_BUCKET_NAME="${s3_bucket_name}"
export AWS_DEFAULT_REGION="${aws_region}"

echo "EC2 ready. Deploy via GitHub Actions." > /home/ec2-user/status.txt
