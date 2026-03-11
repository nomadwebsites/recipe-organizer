# 🍳 Recipe Organizer - Quick Reference Card

## 📍 Your Setup
- **GitHub**: https://github.com/nomadwebsites/recipe-organizer
- **VM**: Ubuntu 22.04 LTS at 192.168.68.144
- **Access**: http://192.168.68.144:5000 (or :80 with nginx)

## 🚀 Quick Deploy/Update

```bash
# SSH to VM
ssh your-username@192.168.68.144

# Update app
cd /opt/recipe-organizer
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart recipe-organizer

# Check status
sudo systemctl status recipe-organizer
```

## 📋 3 Ways to Add Recipes

### 1. 📋 Paste Recipe (Works with ANY site!)
- Copy recipe from ANY website
- Click "📋 Paste Recipe" button
- Paste and click "Parse Recipe"
- Claude AI extracts everything!

### 2. 🌐 Import from URL (Best for blogs)
- Click "Import from URL"
- Paste URL (Budget Bytes, King Arthur, etc.)
- Wait 2-5 seconds
- Review and save

### 3. ✏️ Manual Entry
- Click "Add Recipe"
- Fill in the form
- Save

## 🔍 Search Tips

```
"chicken"          → Find chicken recipes
"quick dinner"     → Find quick dinners
"tomatoes garlic"  → Find recipes with both
"vegetarian"       → Find vegetarian recipes
```

## 🛠️ Useful Commands

```bash
# View logs
sudo journalctl -u recipe-organizer -f

# Restart
sudo systemctl restart recipe-organizer

# Setup nginx (remove :5000 from URL)
sudo bash /opt/recipe-organizer/setup-nginx.sh

# Backup database
cp /opt/recipe-organizer/recipes.db ~/backup.db

# Check if running
sudo netstat -tulpn | grep 5000
```

## 🔑 API Key Setup

1. Get key: https://console.anthropic.com/
2. Edit: `nano /opt/recipe-organizer/.env`
3. Add: `ANTHROPIC_API_KEY=sk-ant-your-key-here`
4. Restart: `sudo systemctl restart recipe-organizer`

## 📚 Documentation

- **START_HERE.md** - Quick overview
- **COMPLETE_GUIDE.md** - Full guide
- **DEPLOYMENT_UPDATE.md** - Update instructions
- **FEATURES.md** - Feature showcase
- **TROUBLESHOOTING** - See COMPLETE_GUIDE.md

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't import URL | Use "📋 Paste Recipe" instead |
| Service won't start | Check logs: `sudo journalctl -u recipe-organizer -n 50` |
| API key error | Verify `.env` file |
| Port in use | Change PORT in `.env` |
| Can't access remotely | `sudo ufw allow 5000/tcp` |

## ✅ What Works

**Import from URL** ✅
- Budget Bytes ⭐
- King Arthur Baking
- Simply Recipes
- Most food blogs

**Paste Recipe** ✅
- AllRecipes
- Food Network
- NYT Cooking
- **ANY website!**

## 🎯 Key Features

✅ Browse all recipes in grid  
✅ Full-text search  
✅ Manual entry  
✅ URL import (supported sites)  
✅ Paste & parse (ANY site)  
✅ Edit recipes  
✅ Delete recipes  
✅ Tag organization  
✅ Mobile responsive  

## 📞 Quick Help

1. Check logs: `sudo journalctl -u recipe-organizer -f`
2. Restart: `sudo systemctl restart recipe-organizer`
3. Read: `/opt/recipe-organizer/COMPLETE_GUIDE.md`

---

**Built with Python + Flask + SQLite + Claude AI**

Happy Cooking! 🍳👨‍🍳
