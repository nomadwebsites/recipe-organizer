#!/bin/bash

# Setup Nginx reverse proxy for Recipe Organizer
# This allows access without specifying port :5000

set -e

echo "=========================================="
echo "Recipe Organizer - Nginx Setup"
echo "=========================================="
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo:"
    echo "sudo ./setup-nginx.sh"
    exit 1
fi

# Install Nginx if not already installed
echo "Step 1: Installing Nginx..."
apt-get update -qq
apt-get install -y nginx

# Stop Nginx temporarily
echo ""
echo "Step 2: Configuring Nginx..."
systemctl stop nginx

# Copy configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp "$SCRIPT_DIR/nginx-recipe-organizer.conf" /etc/nginx/sites-available/recipe-organizer

# Remove default site if it exists
if [ -f /etc/nginx/sites-enabled/default ]; then
    echo "Removing default Nginx site..."
    rm /etc/nginx/sites-enabled/default
fi

# Enable our site
ln -sf /etc/nginx/sites-available/recipe-organizer /etc/nginx/sites-enabled/

# Test Nginx configuration
echo ""
echo "Step 3: Testing Nginx configuration..."
nginx -t

# Start Nginx
echo ""
echo "Step 4: Starting Nginx..."
systemctl start nginx
systemctl enable nginx

# Check status
echo ""
echo "Step 5: Checking status..."
systemctl status nginx --no-pager -l

echo ""
echo "=========================================="
echo "✅ Nginx Setup Complete!"
echo "=========================================="
echo ""
echo "Your Recipe Organizer is now accessible at:"
echo "  http://$(hostname -I | awk '{print $1}')"
echo ""
echo "No port number needed!"
echo ""
echo "Nginx will forward requests to Flask running on port 5000"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status nginx       # Check Nginx status"
echo "  sudo systemctl restart nginx      # Restart Nginx"
echo "  sudo tail -f /var/log/nginx/recipe-organizer-access.log  # View access logs"
echo "  sudo tail -f /var/log/nginx/recipe-organizer-error.log   # View error logs"
echo ""
