# Recipe Organizer - Project Summary

## Overview
A full-stack web application for organizing and managing recipes with AI-powered URL import capabilities. Built specifically for deployment on Ubuntu 22.04 LTS (Proxmox VM).

## Key Features Implemented

### ✅ Core Functionality
- **Browse & View Recipes**: Beautiful grid layout with recipe cards
- **Full-Text Search**: Search across recipe names, ingredients, descriptions, and instructions
- **CRUD Operations**: Create, Read, Update, Delete recipes
- **Manual Entry**: Add recipes with detailed information (ingredients, instructions, timing, servings, tags)
- **URL Import**: AI-powered recipe extraction from websites using Claude API
- **Image Support**: Display recipe images from URLs
- **Tags System**: Organize recipes with custom tags
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 🛠️ Technical Stack

**Backend:**
- Flask 3.0.0 - Web framework
- SQLite with FTS5 - Database with full-text search
- Anthropic Claude API - AI recipe parsing
- BeautifulSoup4 - HTML parsing
- Gunicorn - Production WSGI server

**Frontend:**
- Vanilla JavaScript (no frameworks)
- Modern CSS with gradients and animations
- Responsive grid layout
- Modal dialogs for UX

**Deployment:**
- Systemd service for auto-start
- Nginx reverse proxy support
- SSL/HTTPS ready
- Ubuntu 22.04 LTS optimized

## Project Structure

```
recipe-organizer/
├── app.py                      # Main Flask application
├── database.py                 # Database models and operations
├── recipe_parser.py            # Claude AI integration for URL parsing
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Comprehensive documentation
├── QUICKSTART.md               # Quick start guide
├── PROJECT_SUMMARY.md          # This file
├── deploy.sh                   # Automated deployment script
├── start.sh                    # Quick start script for dev/testing
├── recipe-organizer.service    # Systemd service template
└── static/
    ├── index.html              # Main HTML page
    ├── styles.css              # Stylesheet
    └── app.js                  # Frontend JavaScript
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve the main HTML page |
| GET | `/api/recipes` | Get all recipes |
| GET | `/api/recipes/<id>` | Get a specific recipe |
| POST | `/api/recipes` | Create a new recipe |
| PUT | `/api/recipes/<id>` | Update a recipe |
| DELETE | `/api/recipes/<id>` | Delete a recipe |
| GET | `/api/search?q=<query>` | Search recipes |
| POST | `/api/parse-url` | Parse recipe from URL using AI |

## Database Schema

### recipes table
- `id` - Integer, primary key, auto-increment
- `name` - Text, required
- `description` - Text
- `ingredients` - Text (JSON array)
- `instructions` - Text (JSON array)
- `prep_time` - Text
- `cook_time` - Text
- `servings` - Text
- `source_url` - Text
- `image_url` - Text
- `tags` - Text (JSON array)
- `created_at` - Timestamp
- `updated_at` - Timestamp

### recipes_fts (FTS5 Virtual Table)
Full-text search index on: name, description, ingredients, instructions, tags

## Deployment Options

### Option 1: Quick Start (Development/Testing)
```bash
./start.sh
```
Access at: http://localhost:5000

### Option 2: Automated Production Deployment
```bash
./deploy.sh
```
Installs as systemd service on Ubuntu 22.04 LTS

### Option 3: Manual Production Deployment
Follow the comprehensive guide in README.md

## Configuration

### Required Environment Variables
- `ANTHROPIC_API_KEY` - Your Anthropic API key for Claude AI
- `PORT` - Port to run the application (default: 5000)

### Getting an Anthropic API Key
1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and paste into `.env` file

## Testing Results

### ✅ Tested Features
- ✅ Database initialization
- ✅ Flask server startup
- ✅ Recipe creation via API
- ✅ Recipe retrieval via API
- ✅ Full-text search functionality
- ✅ Frontend page serving
- ✅ All API endpoints responding correctly

### Sample API Test Results

**Get all recipes:**
```bash
curl http://localhost:5000/api/recipes
```

**Create a recipe:**
```bash
curl -X POST http://localhost:5000/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Recipe", "ingredients":["item1"], "instructions":["step1"]}'
```

**Search recipes:**
```bash
curl "http://localhost:5000/api/search?q=chocolate"
```

## Production Deployment Checklist

- [ ] Ubuntu 22.04 LTS VM ready
- [ ] Copy all files to `/opt/recipe-organizer`
- [ ] Install Python 3.10+
- [ ] Create virtual environment
- [ ] Install dependencies from requirements.txt
- [ ] Configure .env with ANTHROPIC_API_KEY
- [ ] Initialize database
- [ ] Set up systemd service
- [ ] Configure firewall (allow port 5000 or 80/443)
- [ ] Optional: Set up Nginx reverse proxy
- [ ] Optional: Configure SSL with Let's Encrypt
- [ ] Test the application
- [ ] Set up database backups

## Security Considerations

### Implemented
- Environment variable for API key (not in code)
- .gitignore for sensitive files
- Input validation on API endpoints
- SQL injection prevention (parameterized queries)

### Recommended
- Use HTTPS in production (via Nginx + Let's Encrypt)
- Restrict firewall to necessary ports only
- Keep ANTHROPIC_API_KEY secure
- Regular database backups
- Consider adding authentication for multi-user scenarios

## Maintenance

### Backup Database
```bash
cp /opt/recipe-organizer/recipes.db ~/recipes-backup-$(date +%Y%m%d).db
```

### View Logs
```bash
sudo journalctl -u recipe-organizer -f
```

### Restart Service
```bash
sudo systemctl restart recipe-organizer
```

### Update Application
```bash
cd /opt/recipe-organizer
git pull  # if using git
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart recipe-organizer
```

## Future Enhancement Ideas

- User authentication and multi-user support
- Recipe categories and advanced filtering
- Meal planning feature
- Shopping list generation
- Print-friendly recipe format
- Recipe rating and favorites
- Recipe sharing via link
- Nutritional information integration
- Unit conversion tool
- Recipe scaling (adjust servings)
- Photo upload capability
- Export recipes to PDF
- Import from other recipe apps
- Recipe collections/cookbooks

## Support Resources

- **Full Documentation**: README.md
- **Quick Start**: QUICKSTART.md
- **Deployment Script**: deploy.sh
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Anthropic API Docs**: https://docs.anthropic.com/
- **SQLite FTS5**: https://www.sqlite.org/fts5.html

## License
MIT License - Free to use and modify

## Credits
Built with Flask, Claude AI, and love for cooking! 🍳

---

**Version**: 1.0.0  
**Date**: March 2026  
**Status**: Production Ready ✅
