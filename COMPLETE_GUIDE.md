# Complete Recipe Organizer Guide

## 🎉 What You Have

A fully functional, production-ready **Recipe Organizer** web application with:

### ✨ Core Features
- 📖 **Browse Recipes**: Beautiful grid layout with images
- 🔍 **Advanced Search**: Full-text search across all recipe fields (name, ingredients, description, instructions)
- ➕ **Manual Entry**: Add recipes with all details (ingredients, instructions, times, servings, tags)
- ✏️ **Edit Recipes**: Update any recipe anytime
- 🗑️ **Delete Recipes**: Remove unwanted recipes
- 🏷️ **Tags**: Organize with custom tags
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

### 🤖 AI-Powered Import Features
1. **Import from URL** (for supported sites)
   - Works great with: Budget Bytes, King Arthur Baking, Simply Recipes, and most food blogs
   - Uses JSON-LD structured data when available (instant!)
   - Falls back to Claude AI for HTML parsing
   
2. **📋 Paste Recipe Text** (works with ANY site!)
   - **NEW!** Works with AllRecipes, Food Network, NYT Cooking, and ANY recipe website
   - Copy recipe text from any website
   - Paste into the app
   - Claude AI extracts all the info automatically
   - Perfect workaround for sites with bot protection

### 🛠️ Technology Stack
- **Backend**: Python 3, Flask
- **Database**: SQLite with FTS5 (Full-Text Search)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla - no frameworks!)
- **AI**: Anthropic Claude 3.5 Sonnet
- **Web Server**: Gunicorn + Nginx (optional)
- **Deployment**: Systemd service

### 📦 What's Included
- Automated deployment scripts
- Systemd service configuration
- Nginx reverse proxy setup
- Database initialization
- Sample data seeder
- Complete documentation

---

## 🚀 Quick Deployment on Your Ubuntu VM

Your VM IP: **192.168.68.144**

### Option A: Update Existing Deployment (If Already Deployed)

```bash
# SSH into your VM
ssh your-username@192.168.68.144

# Navigate to app directory
cd /opt/recipe-organizer

# Pull latest changes
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl restart recipe-organizer

# Check status
sudo systemctl status recipe-organizer
```

**Access**: http://192.168.68.144:5000

### Option B: Fresh Installation

See **README.md** for complete step-by-step installation instructions.

Quick version:
```bash
# Clone repository
sudo mkdir -p /opt/recipe-organizer
sudo chown $USER:$USER /opt/recipe-organizer
cd /opt/recipe-organizer
git clone https://github.com/nomadwebsites/recipe-organizer.git .

# Run automated deployment
./deploy.sh

# Follow the prompts to enter your Anthropic API key
```

---

## 🌐 Optional: Remove Port Number from URL

Want to access at `http://192.168.68.144` instead of `http://192.168.68.144:5000`?

Run this one command:
```bash
cd /opt/recipe-organizer
sudo bash setup-nginx.sh
```

Done! Now access at: **http://192.168.68.144**

---

## 🔑 Getting Your Anthropic API Key

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-`)
6. Add to `/opt/recipe-organizer/.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   PORT=5000
   ```

### Pricing
- Claude API is pay-as-you-go
- Parsing one recipe ≈ $0.01-0.03
- 100 imports ≈ $1-3
- Very affordable for personal use!

---

## 📖 How to Use

### Method 1: Import from URL (Supported Sites)

1. Click **"Import from URL"** button
2. Paste a recipe URL from:
   - Budget Bytes (budgetbytes.com) ✅
   - King Arthur Baking (kingarthurbaking.com) ✅
   - Simply Recipes (simplyrecipes.com) ✅
   - Most food blogs ✅
3. Click **"Import Recipe"**
4. Wait 2-5 seconds
5. Review and save

**Note**: Some major sites (AllRecipes, Food Network) may block automated requests. Use Method 2 instead!

### Method 2: Paste Recipe Text (Works with ANY Site!) 📋

1. Open the recipe in your web browser (ANY site!)
2. Select all the recipe text (Ctrl+A or Cmd+A)
3. Copy (Ctrl+C or Cmd+C)
4. In Recipe Organizer, click **"📋 Paste Recipe"** button
5. Paste the text (Ctrl+V or Cmd+V)
6. Click **"Parse Recipe"**
7. Claude AI extracts the info automatically!
8. Review and save

**This method works with**:
- AllRecipes ✅
- Food Network ✅
- NYT Cooking ✅
- Taste of Home ✅
- ANY recipe website ✅

### Method 3: Manual Entry

1. Click **"Add Recipe"** button
2. Fill in the form:
   - Recipe Name (required)
   - Description
   - Ingredients (one per line, required)
   - Instructions (one step per line, required)
   - Prep Time (e.g., "15 minutes")
   - Cook Time (e.g., "30 minutes")
   - Servings (e.g., "4 servings")
   - Tags (comma-separated, e.g., "dinner, vegetarian, quick")
   - Image URL (optional)
3. Click **"Save Recipe"**

### Searching Recipes

Just type in the search box:
- Recipe name: `"chicken parmesan"`
- Ingredient: `"tomatoes"`
- Type: `"vegetarian"`
- Tag: `"quick"`

Press Enter or click Search. Results are instant!

### Editing/Deleting

1. Click on any recipe card to view details
2. Click **"Edit"** to modify
3. Click **"Delete"** to remove

---

## 📁 Project Structure

```
/opt/recipe-organizer/
├── app.py                    # Main Flask application
├── database.py               # Database initialization
├── recipe_parser.py          # AI parsing logic
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API key)
├── recipes.db               # SQLite database
├── static/
│   ├── index.html           # Frontend HTML
│   ├── app.js               # Frontend JavaScript
│   └── styles.css           # Frontend CSS
├── deploy.sh                # Automated deployment script
├── setup-nginx.sh           # Nginx setup script
├── start.sh                 # Development server script
├── nginx-recipe-organizer.conf  # Nginx configuration
└── recipe-organizer.service     # Systemd service file
```

---

## 🔧 Maintenance

### View Logs
```bash
# Application logs
sudo journalctl -u recipe-organizer -f

# Or app file logs
tail -f /opt/recipe-organizer/app.log

# Nginx access logs (if using nginx)
sudo tail -f /var/log/nginx/recipe-organizer-access.log
```

### Restart Service
```bash
sudo systemctl restart recipe-organizer
```

### Backup Database
```bash
cp /opt/recipe-organizer/recipes.db ~/recipe-backup-$(date +%Y%m%d).db
```

### Update Application
```bash
cd /opt/recipe-organizer
git pull origin main
source venv/bin/activate
pip install --upgrade -r requirements.txt
sudo systemctl restart recipe-organizer
```

---

## 📚 Documentation Files

- **README.md** - Complete installation and setup guide
- **QUICKSTART.md** - Quick start for local development
- **DEPLOYMENT_UPDATE.md** - How to update deployed app
- **NGINX_SETUP.md** - Nginx reverse proxy setup
- **RECIPE_SITES.md** - Which websites work best
- **PROJECT_SUMMARY.md** - Technical overview
- **FILES_OVERVIEW.txt** - File-by-file explanation

---

## 🐛 Troubleshooting

### Service won't start
```bash
sudo journalctl -u recipe-organizer -n 50
```

### Port already in use
```bash
sudo netstat -tulpn | grep 5000
# Kill the process or change PORT in .env
```

### Import not working
- Check your ANTHROPIC_API_KEY in `.env`
- Try the "Paste Recipe Text" method instead
- Check logs for error messages

### Can't access from other devices
```bash
# Check firewall
sudo ufw allow 5000/tcp
sudo ufw allow 80/tcp  # If using nginx
```

### Database issues
```bash
# Backup current database
cp recipes.db recipes.db.backup

# Reinitialize
python3 -c "import database; database.init_db()"
```

---

## 🎯 Usage Tips

1. **For protected sites**: Use the "📋 Paste Recipe" feature - it works every time!

2. **Batch importing**: Open multiple tabs, copy/paste multiple recipes quickly

3. **Organization**: Use tags like "quick", "vegetarian", "dessert" for easy filtering

4. **Search**: Search by ingredient to find recipes you can make with what you have

5. **Backup**: Regularly backup your `recipes.db` file

6. **Mobile**: Access from your phone while cooking! Responsive design works great.

---

## 🔐 Security Notes

- Keep your `.env` file secure
- Never commit `.env` to version control
- The ANTHROPIC_API_KEY should remain private
- Consider using HTTPS with Let's Encrypt for production
- Regular backups recommended

---

## 🎨 Customization Ideas

### Add More Features
- Meal planning calendar
- Shopping list generator
- Nutrition information
- Recipe ratings and reviews
- Recipe sharing with friends
- Export to PDF

### Modify the Look
Edit `static/styles.css` to change:
- Color scheme
- Fonts
- Layout
- Card sizes

### Add More Tags
Edit recipes to include tags like:
- Cuisine: italian, mexican, indian, thai
- Difficulty: easy, medium, hard
- Diet: vegan, keto, paleo, gluten-free
- Meal: breakfast, lunch, dinner, snack
- Season: summer, winter, holiday

---

## 📞 Support

### GitHub Repository
https://github.com/nomadwebsites/recipe-organizer

### Common Issues
1. **403 errors on imports**: Use "Paste Recipe Text" feature
2. **API key errors**: Check `.env` file format
3. **Service crashes**: Check logs with `journalctl`
4. **Nginx issues**: Run `sudo nginx -t` to test config

---

## 🎉 What's New in Latest Version

### Version 1.1.0 (Latest)
- ✨ **NEW**: "Paste Recipe Text" feature - works with ANY website!
- 🔧 Improved cloudscraper integration for better bot protection bypass
- 🐛 Fixed static file serving issues
- 📚 Enhanced documentation with site compatibility guide
- 🚀 Automated nginx setup script
- 💾 Better error messages and logging

### Version 1.0.0
- Initial release
- Basic CRUD operations
- URL import with Claude AI
- Full-text search
- Responsive design

---

## 📋 Quick Reference

### Access URLs
- **With port**: http://192.168.68.144:5000
- **Without port** (with nginx): http://192.168.68.144

### Important Commands
```bash
# Start/Stop/Restart
sudo systemctl start recipe-organizer
sudo systemctl stop recipe-organizer
sudo systemctl restart recipe-organizer

# View logs
sudo journalctl -u recipe-organizer -f

# Update app
cd /opt/recipe-organizer && git pull && sudo systemctl restart recipe-organizer

# Backup database
cp /opt/recipe-organizer/recipes.db ~/recipes-backup.db
```

### API Endpoints
- `GET /api/recipes` - List all recipes
- `GET /api/recipes/<id>` - Get one recipe
- `POST /api/recipes` - Create recipe
- `PUT /api/recipes/<id>` - Update recipe
- `DELETE /api/recipes/<id>` - Delete recipe
- `GET /api/search?q=<query>` - Search recipes
- `POST /api/parse-url` - Parse recipe from URL
- `POST /api/parse-text` - Parse recipe from text

---

## 🏆 Success!

You now have a fully functional Recipe Organizer running on your Proxmox VM!

**Next Steps**:
1. SSH into your VM
2. Run the update commands from DEPLOYMENT_UPDATE.md
3. Set up nginx for port-free access (optional)
4. Start importing your favorite recipes!

**Happy Cooking!** 🍳👨‍🍳🎉

---

*Built with ❤️ using Flask, SQLite, and Claude AI*
