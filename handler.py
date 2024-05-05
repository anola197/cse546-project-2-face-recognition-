import json
import boto3
import cv2
import os
from PIL import Image, ImageDraw, ImageFont
from facenet_pytorch import MTCNN, InceptionResnetV1
from shutil import rmtree
import numpy as np
import torch
#from face_recognition_code import face_recognition_function as face_recognition

AWS_ACCESS_KEY_ID = "AKIAVRUVQFBTU62ZI2VZ"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_REGION = "us-east-1"
ASU_ID = "1229331326"
os.environ['TORCH_HOME'] = '/tmp/torch'


mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # initializing mtcnn for face detection
resnet = InceptionResnetV1(pretrained='vggface2').eval() # initializing resnet for face img to embeding conversion

def face_recognition_function(key_path,s3_client):
    pt_file_path = "/tmp/data.pt"
    s3_client.download_file('classificationresults', 'data.pt', pt_file_path)
    # Face extraction
    img = cv2.imread(key_path, cv2.IMREAD_COLOR)
    boxes, _ = mtcnn.detect(img)

    # Face recognition
    key = os.path.splitext(os.path.basename(key_path))[0].split(".")[0]
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    face, prob = mtcnn(img, return_prob=True, save_path=None)
    saved_data = torch.load(pt_file_path)  # loading data.pt file
    if face != None:
        emb = resnet(face.unsqueeze(0)).detach()  # detech is to make required gradient false
        embedding_list = saved_data[0]  # getting embedding data
        name_list = saved_data[1]  # getting list of names
        dist_list = []  # list of matched distances, minimum distance is used to identify the person
        for idx, emb_db in enumerate(embedding_list):
            dist = torch.dist(emb, emb_db).item()
            dist_list.append(dist)
        idx_min = dist_list.index(min(dist_list))

        # Save the result name in a file
        with open("/tmp/" + key + ".txt", 'w+') as f:
            f.write(name_list[idx_min])
        return name_list[idx_min]
    else:
        print(f"No face is detected")
    return

def handler(event, context):
    try:
        s3_client = boto3.client('s3', region_name=AWS_DEFAULT_REGION,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        bucket = event['bucket_name']
        key = event['image_file_name']
        image_path = f'/tmp/{key}'

        s3_client.download_file(bucket, key, image_path)
        recognized_name = face_recognition_function(image_path,s3_client)
        print(f"Recognized face as {recognized_name}")
            
        # Save the recognized name back to S3
        folder_name = os.path.splitext(os.path.basename(key))[0]
        output_prefix = f'{folder_name}/'
        output_key = output_prefix + f"{os.path.splitext(key)[0]}.txt"
        s3_client.put_object(Bucket=f'{ASU_ID}-output', Key=output_key, Body=recognized_name)
        return {
            'statusCode': 200,
            'body': 'Face recognition completed successfully'
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': e
        }

