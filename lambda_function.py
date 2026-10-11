import json
import boto3
import time

def lambda_handler(event, context):
    # Extract S3 bucket and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # EC2 Instance ID
    instance_id = 'i-057b13ac70b9b7893'

    # SSM client
    ssm = boto3.client('ssm', region_name='us-east-1')

    # Command to run on EC2
    command = f"""
    cd /home/ubuntu/yolov5 && \
    git config --global --add safe.directory /home/ubuntu/yolov5 && \
    aws s3 cp s3://{bucket}/{key} /tmp/dog1.jpg && \
    python3 detect.py \
        --weights yolov5s.pt \
        --source /tmp/dog1.jpg \
        --data data/coco128.yaml \
        --imgsz 640 640 \
        --conf-thres 0.25 \
        --iou-thres 0.45 \
        --max-det 1000 \
        --project /tmp/yolo_output \
        --name run \
        --exist-ok \
        --save-txt \
        --line-thickness 3 && \
    aws s3 cp /tmp/yolo_output/run/dog1.jpg \
        s3://{bucket}/results/{key} && \
    aws s3 cp /tmp/yolo_output/run/labels/dog1.txt \
        s3://{bucket}/results/labels/dog1.txt
    """

    # Send SSM RunCommand to EC2
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [command]},
        TimeoutSeconds=55
    )

    command_id = response['Command']['CommandId']

    # Wait for command to complete
    time.sleep(30)

    # Get command result
    output = ssm.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'YOLOv5 detection triggered',
            'bucket': bucket,
            'key': key,
            'command_id': command_id,
            'status': output['Status'],
            'stdout': output['StandardOutputContent'],
            'stderr': output['StandardErrorContent']
        })
    }
