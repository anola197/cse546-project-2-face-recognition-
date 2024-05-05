import boto3
import os
import subprocess
import ffmpeg
import math
import json
from video_splitting_cmdline import video_splitting_cmdline

AWS_ACCESS_KEY_ID = "AKIAVRUVQFBTU62ZI2VZ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"
ASU_ID = "1229331326"

def lambda_handler(event, context):
    s3_client = boto3.client('s3', region_name=AWS_DEFAULT_REGION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                  
    # Retrieve the bucket name and file name from the Lambda event trigger
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        video_key = record['s3']['object']['key']
        download_path = f'/tmp/{video_key}'
        
        # Download the video from S3 to the local file system (Lambda /tmp directory)
        s3_client.download_file(bucket, key, download_path)

        # Extract a frame using FFmpeg
        output_frame_path = video_splitting_cmdline(download_path)

        # Upload the extracted frame back to S3 in the stage-1 bucket
        output_bucket = f"{bucket.split('-')[0]}-stage-1"  # Assuming bucket naming convention
        output_key = os.path.basename(output_frame_path)
        s3_client.upload_file(f"/tmp/{output_frame_path}", output_bucket, output_key)
        
        # Trigger the face-recognition function asynchronously
        invoke_face_recognition(output_bucket, output_key)
        
def invoke_face_recognition(bucket_name, image_file_name):
    lambda_client = boto3.client('lambda', region_name=AWS_DEFAULT_REGION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    payload = {
        'bucket_name': bucket_name,
        'image_file_name': image_file_name
    }

    lambda_client.invoke(
        FunctionName='face-recognition',
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
        


