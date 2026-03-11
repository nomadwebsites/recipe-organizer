# Deployment Update Guide

## Quick Update on Your Ubuntu VM

Follow these steps to update your Recipe Organizer app on your Ubuntu 22.04 LTS VM at `192.168.68.144`.

### Step 1: SSH into Your VM

```bash
ssh your-username@192.168.68.144
```

### Step 2: Navigate to the Application Directory

```bash
cd /opt/recipe-organizer
```

### Step 3: Pull Latest Changes from GitHub

```bash
git pull origin main
```

### Step 4: Update Python Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Restart the Application Service

```bash
sudo systemctl restart recipe-organizer
```

### Step 6: Check Service Status

```bash
sudo systemctl status recipe-organizer
```

You should see "active (running)" in green.

### Step 7: Test the Application

Open your browser and go to:
```
http://192.168.68.144:5000
```

Try the new **"📋 Paste Recipe"** button! This feature works with ANY recipe website:

1. Click "📋 Paste Recipe"
2. Open any recipe website in another tab (even AllRecipes or Food Network)
3. Select all the recipe text (Ctrl+A or Cmd+A)
4. Copy (Ctrl+C or Cmd+C)
5. Paste into the text box
6. Click "Parse Recipe"
7. Claude AI will extract the recipe info!

---

## Optional: Setup Nginx for Port-Free Access

If you want to access the app without specifying `:5000` in the URL, run this command:

```bash
cd /opt/recipe-organizer
sudo bash setup-nginx.sh
```

After this, you can access the app at:
```
http://192.168.68.144
```

(No port number needed!)

---

## What's New?

### ✨ New Features

1. **Paste Recipe Text Button**: Works with ANY recipe website! Copy/paste recipe text and Claude AI will parse it.
2. **Improved Bot Protection Bypass**: Better success rate with recipe websites
3. **Better Error Messages**: More helpful feedback when imports fail
4. **Site Compatibility Guide**: See `RECIPE_SITES.md` for which sites work best

### 🐛 Bug Fixes

- Fixed static file serving issues
- Improved JSON-LD structured data extraction
- Enhanced cloudscraper integration

---

## Troubleshooting

### If the service fails to restart:

Check the logs:
```bash
sudo journalctl -u recipe-organizer -n 50
```

### If you see dependency errors:

Make sure you're in the virtual environment:
```bash
source /opt/recipe-organizer/venv/bin/activate
pip install --upgrade -r requirements.txt
```

### If the app won't load in browser:

Check if it's running:
```bash
sudo netstat -tulpn | grep 5000
```

Check firewall:
```bash
sudo ufw status
sudo ufw allow 5000/tcp
```

---

## Need Help?

- Check logs: `sudo journalctl -u recipe-organizer -f`
- View app logs: `tail -f /opt/recipe-organizer/app.log`
- Check GitHub: https://github.com/nomadwebsites/recipe-organizer

---

Happy cooking! 🍳👨‍🍳
