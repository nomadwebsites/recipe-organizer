# Quick Start Guide

## For Local Testing/Development

### 1. Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### 2. Get an Anthropic API Key
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

### 3. Run the Application

```bash
# Clone or download the recipe-organizer folder
cd recipe-organizer

# Run the start script
./start.sh
```

The start script will:
- Create a Python virtual environment
- Install all dependencies
- Initialize the database
- Start the Flask development server

### 4. Configure API Key

Edit the `.env` file and add your Anthropic API key:

```bash
nano .env
```

Replace `your_anthropic_api_key_here` with your actual API key:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxx
PORT=5000
```

### 5. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## For Production Deployment on Ubuntu 22.04 LTS

See the main **README.md** for detailed production deployment instructions including:
- Systemd service setup
- Nginx reverse proxy configuration
- SSL/HTTPS setup with Let's Encrypt
- Firewall configuration

Or use the automated deployment script:

```bash
./deploy.sh
```

## Testing the Features

### Add a Recipe Manually
1. Click "Add Recipe"
2. Fill in the form
3. Click "Save Recipe"

### Import from URL
1. Click "Import from URL"
2. Paste a recipe URL (e.g., from AllRecipes.com)
3. Click "Import Recipe"
4. Wait a few seconds for Claude AI to parse it
5. Review and save

### Search Recipes
1. Type keywords in the search box
2. Press Enter or click "Search"
3. Results will appear instantly

### Edit/Delete
1. Click on any recipe card
2. Use the "Edit" or "Delete" buttons

## Troubleshooting

### Port Already in Use
Edit `.env` and change the PORT to something else:
```
PORT=8080
```

### API Key Error
Make sure your ANTHROPIC_API_KEY in `.env` is valid and has no extra spaces.

### Database Issues
If you have database corruption, delete `recipes.db` and restart the app. It will create a fresh database.

## Stopping the Application

Press `Ctrl+C` in the terminal where the app is running.

## Data Backup

Your recipes are stored in `recipes.db`. To backup:

```bash
cp recipes.db recipes-backup-$(date +%Y%m%d).db
```

Enjoy your Recipe Organizer! 🍳
