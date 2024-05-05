# AWS Lambda Video Analysis Application
This repository contains a Python-based cloud video analysis application designed for the [CSE 546] Cloud Computing course at Arizona State University. The application leverages AWS Lambda to process video uploads and perform face recognition on extracted frames.

## Project Overview
The application automates video processing by integrating AWS Lambda functions and S3 buckets, implementing a scalable solution for video frame analysis using cloud resources.

### Architecture
<img align="center" alt="Coding" width="900" height ="500" src="documents/architecture .png">
The solution architecture utilizes AWS Lambda for processing and AWS S3 for storage:

1. **Input Bucket:** Receives video uploads.
2. **Video-Splitting Function:** Splits uploaded videos into frames and stores them in the Stage-1 Bucket using FFmpeg.
3. **Face-Recognition Function:** Performs face recognition on the frames using a pre-trained CNN model (ResNet) and saves the results to the Output Bucket.

## Setup and Deployment

### Prerequisites

- AWS Account
- Python 3.8 or higher
- AWS CLI configured with appropriate permissions

### Deployment Steps

1. Deploy the **Video-Splitting Function** using Lambda UI:
- Create a .zip file containing your Python code and dependencies. (ffmpeg package)
- Upload this .zip file as a new layer in AWS Lambda.
- Configure your Lambda function to use this layer.

2. Deploy the **Face-Recognition Function** using Docker:
- Build the Docker image: `docker build -t face-recognition .`
- Tag and push the Docker image to AWS ECR:
  - `aws ecr create-repository --repository-name face-recognition`
  - `docker tag face-recognition:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/face-recognition:latest`
  - `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com`
  - `docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/face-recognition:latest`
- Create a Lambda function from the Docker image
