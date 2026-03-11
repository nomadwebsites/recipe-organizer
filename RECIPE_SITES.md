# Recipe Site Compatibility

This document lists which recipe websites work best with the URL import feature.

## ✅ Works Great (JSON-LD Structured Data)

These sites provide machine-readable recipe data that works perfectly:

- **Budget Bytes** (budgetbytes.com) ✓ Tested
- **Food Network** (foodnetwork.com)
- **Bon Appétit** (bonappetit.com)
- **Epicurious** (epicurious.com)
- **Tasty** (tasty.co)
- **Delish** (delish.com)
- **The Kitchn** (thekitchn.com)
- **Sally's Baking Addiction** (sallysbakingaddiction.com)
- **King Arthur Baking** (kingarthurbaking.com)
- **Minimalist Baker** (minimalistbaker.com)
- **Gimme Some Oven** (gimmesomeoven.com)
- **Damn Delicious** (damndelicious.net)
- **Pinch of Yum** (pinchofyum.com)
- **Half Baked Harvest** (halfbakedharvest.com)
- **Love and Lemons** (loveandlemons.com)
- **Cookie and Kate** (cookieandkate.com)
- **Smitten Kitchen** (smittenkitchen.com)
- **Simply Recipes** (simplyrecipes.com)
- **Spend with Pennies** (spendwithpennies.com)

## ⚠️ May Work (Sometimes Protected)

These sites sometimes use bot protection but may work:

- **AllRecipes** (allrecipes.com) - Hit or miss
- **Serious Eats** (seriouseats.com) - Protected by Cloudflare
- **NYT Cooking** (cooking.nytimes.com) - Requires subscription
- **Taste of Home** (tasteofhome.com) - Sometimes blocked

## 🔄 Workarounds for Protected Sites

If you get a 403 error:

### Option 1: Manual Entry
1. Open the recipe in your browser
2. Copy the recipe information
3. Click "Add Recipe" in Recipe Organizer
4. Paste the information manually

### Option 2: Try a Different Recipe
- Many recipes are duplicated across sites
- Search for the recipe name on a more bot-friendly site

### Option 3: Browser Extension (Future Feature)
- Could create a browser extension that extracts recipes as you browse
- The extension runs in your browser, so no bot detection

## 🧪 Testing a Site

To test if a site works with our app:

```bash
cd /opt/recipe-organizer
source venv/bin/activate
python3 << 'EOF'
import recipe_parser

url = "YOUR_RECIPE_URL_HERE"
try:
    result = recipe_parser.parse_recipe_with_claude(url)
    print(f"✓ Works! Recipe: {result['name']}")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

## 📊 Why Some Sites Block Bots

Recipe websites block automated requests because:
- **Revenue**: They want you to see ads on their website
- **Analytics**: They track user behavior and clicks
- **Security**: Protection against scraping and DDOS attacks

## 🤖 How Our Import Works

1. **JSON-LD First**: Most modern recipe sites include structured data in JSON-LD format (designed for machines!)
2. **No AI Needed**: JSON-LD extraction is instant and free
3. **Claude AI Fallback**: If JSON-LD isn't available, Claude reads the page content
4. **Smart Headers**: We rotate user agents to appear as a regular browser

## 💡 Tip: Finding Good Recipe Sources

Look for:
- **Food blogs** rather than major publications
- **Smaller recipe sites** that focus on content over ads
- **Sites optimized for Google** (they usually have good JSON-LD)

Avoid:
- Sites with paywalls
- Sites with heavy ads and popups
- Major news sites (they protect content aggressively)

## 📝 Contributing

Found a site that works or doesn't work? Let us know by opening an issue on GitHub!
