# AWS Lambda Video Analysis Application

This repository contains a Python-based cloud video analysis application designed for the [CSE 546] Cloud Computing course at Arizona State University. The application leverages AWS Lambda to process video uploads and perform face recognition on extracted frames.

## Project Overview

The application automates video processing by integrating AWS Lambda functions and S3 buckets, implementing a scalable solution for video frame analysis using cloud resources.

### Architecture

The solution architecture utilizes AWS Lambda for processing and AWS S3 for storage:

1. **Input Bucket:** Receives video uploads.
2. **Video-Splitting Function:** Splits uploaded videos into frames and stores them in the Stage-1 Bucket using FFmpeg.
3. **Face-Recognition Function:** Performs face recognition on the frames using a pre-trained CNN model (ResNet) and saves the results to the Output Bucket.

## Setup and Deployment

### Prerequisites

- AWS Account
- Python 3.8 or higher
- AWS CLI configured with appropriate permissions

### Configuration Steps

