# 🍳 Recipe Organizer - START HERE

Welcome to your Recipe Organizer app! This is a complete, production-ready web application.

## 🎯 What You Need to Know

### For Your Ubuntu VM (192.168.68.144)

**If you haven't deployed yet**, read: [`README.md`](README.md) for full installation

**If already deployed**, to update:

```bash
ssh your-username@192.168.68.144
cd /opt/recipe-organizer
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart recipe-organizer
```

**To enable port-free access** (http://192.168.68.144 instead of :5000):

```bash
sudo bash setup-nginx.sh
```

## 📚 Documentation

### Quick Start
- **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** ⭐ **START HERE** - Everything in one place
- **[QUICKSTART.md](QUICKSTART.md)** - Local development setup
- **[DEPLOYMENT_UPDATE.md](DEPLOYMENT_UPDATE.md)** - How to update your VM

### Detailed Guides
- **[README.md](README.md)** - Full installation instructions
- **[NGINX_SETUP.md](NGINX_SETUP.md)** - Nginx reverse proxy setup
- **[RECIPE_SITES.md](RECIPE_SITES.md)** - Which websites work best

### Technical
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture overview
- **[FILES_OVERVIEW.txt](FILES_OVERVIEW.txt)** - What each file does

## ✨ Key Features

### 1. Manual Recipe Entry
Add recipes with:
- Name, description, ingredients, instructions
- Prep time, cook time, servings
- Tags for organization
- Image URLs

### 2. Import from URL (Supported Sites)
- Budget Bytes ✅
- King Arthur Baking ✅
- Simply Recipes ✅
- Most food blogs ✅

### 3. 📋 Paste Recipe Text (NEW! Works with ANY site)
Perfect for:
- AllRecipes ✅
- Food Network ✅
- NYT Cooking ✅
- **ANY recipe website** ✅

Just copy/paste the recipe text, Claude AI extracts everything!

### 4. Advanced Search
Search by:
- Recipe name
- Ingredients
- Description
- Instructions
- Tags

## 🔑 Important: API Key Required

You need an Anthropic API key for AI-powered imports:

1. Get key at: https://console.anthropic.com/
2. Add to `/opt/recipe-organizer/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

**Cost**: ~$0.01-0.03 per recipe import (very affordable!)

## 🚀 Quick Access

After deployment:
- **With port**: http://192.168.68.144:5000
- **Without port** (after nginx setup): http://192.168.68.144

## 🆘 Getting Help

### Check Status
```bash
sudo systemctl status recipe-organizer
```

### View Logs
```bash
sudo journalctl -u recipe-organizer -f
```

### Restart App
```bash
sudo systemctl restart recipe-organizer
```

### Common Issues
1. **Can't import from URL**: Try the "📋 Paste Recipe" feature instead
2. **API key error**: Check `.env` file format
3. **Port in use**: Change PORT in `.env`
4. **Service won't start**: Check logs with `journalctl`

## 🎯 Next Steps

1. **SSH into your VM**
2. **Update the app** (see commands above)
3. **Set up nginx** (optional, for port-free access)
4. **Start importing recipes!**

## 📖 Best Practices

### For Importing Recipes:
1. Try "Import from URL" first (faster!)
2. If you get a 403 error, use "📋 Paste Recipe" instead
3. Always review imported recipes before saving

### For Organization:
1. Use consistent tag names (e.g., "dinner", "dessert", "quick")
2. Add prep/cook times for meal planning
3. Include source URLs to find recipes later

### For Search:
1. Search by ingredient to find recipes with what you have
2. Use tags to filter by meal type
3. Search by cooking time for quick meals

## 🎉 Ready to Use!

Your Recipe Organizer is complete and ready to deploy. Check **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** for full details.

**Happy Cooking!** 🍳👨‍🍳

---

## 📦 GitHub Repository

https://github.com/nomadwebsites/recipe-organizer

---

## 📋 Quick Commands Cheat Sheet

```bash
# Update app
cd /opt/recipe-organizer && git pull && sudo systemctl restart recipe-organizer

# View logs
sudo journalctl -u recipe-organizer -f

# Check status
sudo systemctl status recipe-organizer

# Restart service
sudo systemctl restart recipe-organizer

# Setup nginx (port-free access)
cd /opt/recipe-organizer && sudo bash setup-nginx.sh

# Backup database
cp /opt/recipe-organizer/recipes.db ~/recipe-backup-$(date +%Y%m%d).db

# Check if app is running
sudo netstat -tulpn | grep 5000
```

---

*Built with Flask, SQLite, and Claude AI* ❤️
