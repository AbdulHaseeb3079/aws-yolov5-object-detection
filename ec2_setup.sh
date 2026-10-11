#!/bin/bash
# EC2 Setup Script for YOLOv5 on Ubuntu

# Update system
sudo apt update -y
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Install AWS CLI
sudo apt install awscli -y

# Clone YOLOv5
cd /home/ubuntu
git clone https://github.com/ultralytics/yolov5
cd yolov5

# Install Python dependencies
pip3 install -r requirements.txt

# Fix git safe directory
git config --global --add safe.directory /home/ubuntu/yolov5

# Download YOLOv5s weights
python3 -c "import torch; torch.hub.load('ultralytics/yolov5', 'yolov5s')"

# Install SSM Agent (if not already installed)
sudo snap install amazon-ssm-agent --classic
sudo systemctl enable amazon-ssm-agent
sudo systemctl start amazon-ssm-agent

echo "EC2 YOLOv5 setup complete!"
