#!/bin/bash

# Recipe Organizer Deployment Script for Ubuntu 22.04 LTS
# This script automates the deployment process

set -e

echo "=========================================="
echo "Recipe Organizer Deployment Script"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "Please do not run this script as root"
    exit 1
fi

# Get current username
USERNAME=$(whoami)

echo "Installing as user: $USERNAME"
echo ""

# Install system dependencies
echo "Step 1: Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create application directory
echo ""
echo "Step 2: Setting up application directory..."
APP_DIR="/opt/recipe-organizer"
if [ -d "$APP_DIR" ]; then
    echo "Directory $APP_DIR already exists."
    read -p "Do you want to continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    sudo mkdir -p $APP_DIR
    sudo chown $USERNAME:$USERNAME $APP_DIR
fi

# Copy files if running from different directory
CURRENT_DIR=$(pwd)
if [ "$CURRENT_DIR" != "$APP_DIR" ]; then
    echo "Copying files to $APP_DIR..."
    cp -r * $APP_DIR/
    cd $APP_DIR
fi

# Create virtual environment
echo ""
echo "Step 3: Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo ""
echo "Step 4: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment file
echo ""
echo "Step 5: Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template"
    echo ""
    read -p "Enter your Anthropic API Key: " API_KEY
    sed -i "s/your_anthropic_api_key_here/$API_KEY/" .env
else
    echo ".env file already exists, skipping..."
fi

# Initialize database
echo ""
echo "Step 6: Initializing database..."
python3 -c "import database; database.init_db()"
echo "Database initialized successfully"

# Setup systemd service
echo ""
echo "Step 7: Setting up systemd service..."
cp recipe-organizer.service /tmp/recipe-organizer.service
sed -i "s/YOUR_USERNAME/$USERNAME/g" /tmp/recipe-organizer.service
sudo cp /tmp/recipe-organizer.service /etc/systemd/system/recipe-organizer.service
rm /tmp/recipe-organizer.service

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable recipe-organizer
sudo systemctl start recipe-organizer

# Check service status
echo ""
echo "Step 8: Checking service status..."
sleep 2
sudo systemctl status recipe-organizer --no-pager

# Configure firewall if ufw is active
if sudo ufw status | grep -q "Status: active"; then
    echo ""
    echo "Step 9: Configuring firewall..."
    sudo ufw allow 5000/tcp
    echo "Firewall rule added for port 5000"
fi

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Your Recipe Organizer is now running!"
echo ""
echo "Access it at: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Useful commands:"
echo "  - View logs: sudo journalctl -u recipe-organizer -f"
echo "  - Restart: sudo systemctl restart recipe-organizer"
echo "  - Stop: sudo systemctl stop recipe-organizer"
echo "  - Status: sudo systemctl status recipe-organizer"
echo ""
echo "For Nginx setup and SSL, see README.md"
echo ""
