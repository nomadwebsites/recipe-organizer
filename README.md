# Recipe Organizer

A web-based recipe organizer application with AI-powered URL import capabilities. Built with Flask, SQLite, and Claude AI.

## Features

- 📖 **Browse Recipes**: View all your recipes in a beautiful grid layout
- 🔍 **Search**: Full-text search across recipe names, ingredients, descriptions, and instructions
- ➕ **Add Recipes**: Manually add recipes with ingredients, instructions, prep time, cook time, and more
- ✏️ **Edit Recipes**: Update existing recipes anytime
- 🗑️ **Delete Recipes**: Remove recipes you no longer need
- 🌐 **Import from URL**: Paste a URL from AllRecipes, food blogs, or any recipe website - Claude AI will extract and parse the recipe automatically
- 🏷️ **Tags**: Organize recipes with custom tags
- 📱 **Responsive Design**: Works great on desktop, tablet, and mobile

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite with FTS5 (Full-Text Search)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **AI Integration**: Anthropic Claude API
- **Deployment**: Gunicorn, Systemd

## Prerequisites

- Ubuntu 22.04 LTS
- Python 3.10+
- Anthropic API key (get one at https://console.anthropic.com/)

## Installation on Ubuntu 22.04 LTS

### 1. Update System and Install Dependencies

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

### 2. Create Application Directory

```bash
sudo mkdir -p /opt/recipe-organizer
sudo chown $USER:$USER /opt/recipe-organizer
cd /opt/recipe-organizer
```

### 3. Clone or Copy Application Files

If you have the files in a Git repository:
```bash
git clone <your-repo-url> .
```

Or manually copy all files to `/opt/recipe-organizer/`:
- app.py
- database.py
- recipe_parser.py
- requirements.txt
- .env.example
- static/ (directory with index.html, styles.css, app.js)

### 4. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

```bash
cp .env.example .env
nano .env
```

Edit the `.env` file and add your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
PORT=5000
```

Save and exit (Ctrl+X, then Y, then Enter).

### 7. Initialize Database

```bash
python3 -c "import database; database.init_db()"
```

### 8. Test the Application

```bash
python3 app.py
```

Visit `http://your-server-ip:5000` in your browser. If it works, press Ctrl+C to stop the test server.

### 9. Create Systemd Service

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/recipe-organizer.service
```

Add the following content:

```ini
[Unit]
Description=Recipe Organizer Web Application
After=network.target

[Service]
Type=notify
User=YOUR_USERNAME
Group=YOUR_USERNAME
WorkingDirectory=/opt/recipe-organizer
Environment="PATH=/opt/recipe-organizer/venv/bin"
EnvironmentFile=/opt/recipe-organizer/.env
ExecStart=/opt/recipe-organizer/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Important**: Replace `YOUR_USERNAME` with your actual username (run `whoami` to check).

Save and exit.

### 10. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable recipe-organizer
sudo systemctl start recipe-organizer
```

### 11. Check Service Status

```bash
sudo systemctl status recipe-organizer
```

You should see "active (running)" in green.

### 12. Configure Firewall (if enabled)

```bash
sudo ufw allow 5000/tcp
```

## Accessing the Application

Open your web browser and navigate to:
```
http://your-server-ip:5000
```

Replace `your-server-ip` with your actual server IP address or hostname.

## Optional: Setup with Nginx Reverse Proxy

For production use, it's recommended to use Nginx as a reverse proxy:

### 1. Install Nginx

```bash
sudo apt install nginx -y
```

### 2. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/recipe-organizer
```

Add the following:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your server IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Enable the Site

```bash
sudo ln -s /etc/nginx/sites-available/recipe-organizer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Allow HTTP through Firewall

```bash
sudo ufw allow 'Nginx Full'
```

Now you can access the app at `http://your-domain.com` or `http://your-server-ip` without specifying the port.

## Optional: SSL/HTTPS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Usage

### Adding a Recipe Manually

1. Click "Add Recipe" button
2. Fill in the recipe details (name, ingredients, instructions are required)
3. Click "Save Recipe"

### Importing from URL

1. Click "Import from URL" button
2. Paste a recipe URL (e.g., from AllRecipes, NYT Cooking, food blogs)
3. Click "Import Recipe"
4. Wait for Claude AI to parse the recipe (takes a few seconds)
5. Review and edit the imported data if needed
6. Click "Save Recipe"

### Searching Recipes

1. Type your search query in the search box (e.g., "chicken", "tomatoes", "quick dinner")
2. Click "Search" or press Enter
3. Results will show recipes matching your query

### Editing/Deleting Recipes

1. Click on any recipe card to view details
2. Click "Edit" to modify the recipe
3. Click "Delete" to remove the recipe

## Troubleshooting

### Check Logs

```bash
sudo journalctl -u recipe-organizer -f
```

### Restart Service

```bash
sudo systemctl restart recipe-organizer
```

### Check if Port is in Use

```bash
sudo netstat -tulpn | grep 5000
```

### Database Location

The SQLite database is stored at `/opt/recipe-organizer/recipes.db`

### Backup Database

```bash
cp /opt/recipe-organizer/recipes.db ~/recipes-backup-$(date +%Y%m%d).db
```

## Maintenance

### Update Application

```bash
cd /opt/recipe-organizer
source venv/bin/activate
git pull  # if using git
pip install -r requirements.txt --upgrade
sudo systemctl restart recipe-organizer
```

### View Running Processes

```bash
ps aux | grep gunicorn
```

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- The ANTHROPIC_API_KEY should be kept secret
- Consider using a firewall to restrict access to port 5000
- For production, always use HTTPS with SSL certificates
- Regularly backup your database

## API Endpoints

- `GET /api/recipes` - Get all recipes
- `GET /api/recipes/<id>` - Get a specific recipe
- `POST /api/recipes` - Create a new recipe
- `PUT /api/recipes/<id>` - Update a recipe
- `DELETE /api/recipes/<id>` - Delete a recipe
- `GET /api/search?q=<query>` - Search recipes
- `POST /api/parse-url` - Parse recipe from URL

## License

MIT License - feel free to use and modify as needed!

## Support

For issues or questions, please check the logs and ensure:
1. All dependencies are installed
2. The ANTHROPIC_API_KEY is valid
3. The service is running
4. Firewall allows connections

Enjoy organizing your recipes! 🍳👨‍🍳
