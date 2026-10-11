# ITC5205 Assignment 2 — AWS YOLOv5 Object Detection System

## Overview
A fully cloud-based, serverless image object detection pipeline built on AWS using:
- **YOLOv5** — Real-time object detection model
- **AWS Lambda** — Serverless orchestration
- **API Gateway** — REST API frontend
- **Amazon EC2** — YOLOv5 inference engine
- **Amazon S3** — Image storage and results

## Architecture
User → API Gateway → Lambda → SSM → EC2 (YOLOv5) → S3

## API Endpoint
**POST** `https://pz9trm81cg.execute-api.us-east-1.amazonaws.com/prod/detect`

## Request Body
```json
{
  "Records": [{
    "s3": {
      "bucket": { "name": "yolo-detection-bucket-2026" },
      "object": { "key": "dog1.jpg" }
    }
  }]
}
