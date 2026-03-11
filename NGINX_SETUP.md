# Setting Up Nginx Reverse Proxy

This guide will help you set up Nginx so you can access your Recipe Organizer without specifying the port number.

## Quick Setup (Recommended)

Simply run the automated setup script:

```bash
cd /opt/recipe-organizer
sudo ./setup-nginx.sh
```

That's it! Your app will now be accessible at:
- `http://YOUR-VM-IP` (no port needed!)

---

## What This Does

The Nginx reverse proxy:
- Listens on port 80 (default HTTP port)
- Forwards all requests to your Flask app on port 5000
- Allows you to access the app without `:5000` in the URL
- Improves performance with caching
- Makes it easier to add SSL/HTTPS later

---

## Manual Setup

If you prefer to set up manually:

### 1. Install Nginx
```bash
sudo apt-get update
sudo apt-get install -y nginx
```

### 2. Copy Configuration
```bash
cd /opt/recipe-organizer
sudo cp nginx-recipe-organizer.conf /etc/nginx/sites-available/recipe-organizer
```

### 3. Enable Site
```bash
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
sudo ln -s /etc/nginx/sites-available/recipe-organizer /etc/nginx/sites-enabled/
```

### 4. Test and Restart
```bash
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
sudo systemctl enable nginx  # Start on boot
```

---

## Verification

Test that everything works:

```bash
# Check Nginx status
sudo systemctl status nginx

# Test locally
curl http://localhost

# Test from another machine
curl http://YOUR-VM-IP
```

---

## Adding SSL/HTTPS (Optional)

To enable HTTPS with Let's Encrypt:

```bash
# Install certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Certbot will automatically update your Nginx config!
```

---

## Useful Commands

```bash
# View access logs
sudo tail -f /var/log/nginx/recipe-organizer-access.log

# View error logs
sudo tail -f /var/log/nginx/recipe-organizer-error.log

# Restart Nginx
sudo systemctl restart nginx

# Check configuration syntax
sudo nginx -t

# Reload configuration without downtime
sudo systemctl reload nginx
```

---

## Troubleshooting

### Port 80 already in use
```bash
# Check what's using port 80
sudo netstat -tulpn | grep :80

# Stop conflicting service (if Apache)
sudo systemctl stop apache2
sudo systemctl disable apache2
```

### Nginx won't start
```bash
# Check configuration
sudo nginx -t

# View detailed logs
sudo journalctl -u nginx -n 50

# Check if Flask app is running
sudo systemctl status recipe-organizer
```

### Can't access from other machines
```bash
# Check firewall
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp  # For HTTPS

# On Proxmox, you may also need to allow ports in the web interface
```

---

## Configuration File Location

- Main config: `/etc/nginx/sites-available/recipe-organizer`
- Enabled symlink: `/etc/nginx/sites-enabled/recipe-organizer`
- Source template: `/opt/recipe-organizer/nginx-recipe-organizer.conf`

---

## Customization

To customize the Nginx configuration:

1. Edit the source file:
```bash
nano /opt/recipe-organizer/nginx-recipe-organizer.conf
```

2. Copy to Nginx directory:
```bash
sudo cp /opt/recipe-organizer/nginx-recipe-organizer.conf /etc/nginx/sites-available/recipe-organizer
```

3. Test and reload:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

Common customizations:
- Change `server_name _;` to your domain name
- Adjust `client_max_body_size` for larger uploads
- Add rate limiting
- Configure caching
- Add custom headers
