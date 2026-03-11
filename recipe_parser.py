import os
import json
import requests
from anthropic import Anthropic
from bs4 import BeautifulSoup
import re

def extract_recipe_json_ld(html_content):
    """Extract recipe data from JSON-LD structured data"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all script tags with type application/ld+json
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                
                # Handle both single objects and arrays
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get('@type') == 'Recipe':
                            return item
                elif isinstance(data, dict):
                    if data.get('@type') == 'Recipe':
                        return data
                    # Sometimes it's nested in @graph
                    if '@graph' in data:
                        for item in data['@graph']:
                            if isinstance(item, dict) and item.get('@type') == 'Recipe':
                                return item
            except (json.JSONDecodeError, AttributeError):
                continue
        
        return None
    except Exception as e:
        return None

def parse_recipe_from_json_ld(recipe_data, url):
    """Convert JSON-LD recipe data to our format"""
    parsed = {
        'name': recipe_data.get('name', ''),
        'description': recipe_data.get('description', ''),
        'source_url': url,
        'image_url': None,
        'ingredients': [],
        'instructions': [],
        'prep_time': None,
        'cook_time': None,
        'servings': None,
        'tags': []
    }
    
    # Extract image
    if 'image' in recipe_data:
        img = recipe_data['image']
        if isinstance(img, list) and len(img) > 0:
            parsed['image_url'] = img[0] if isinstance(img[0], str) else img[0].get('url')
        elif isinstance(img, dict):
            parsed['image_url'] = img.get('url')
        elif isinstance(img, str):
            parsed['image_url'] = img
    
    # Extract ingredients
    if 'recipeIngredient' in recipe_data:
        ingredients = recipe_data['recipeIngredient']
        if isinstance(ingredients, list):
            parsed['ingredients'] = ingredients
        elif isinstance(ingredients, str):
            parsed['ingredients'] = [ingredients]
    
    # Extract instructions
    if 'recipeInstructions' in recipe_data:
        instructions = recipe_data['recipeInstructions']
        if isinstance(instructions, list):
            steps = []
            for inst in instructions:
                if isinstance(inst, str):
                    steps.append(inst)
                elif isinstance(inst, dict):
                    if 'text' in inst:
                        steps.append(inst['text'])
                    elif '@type' in inst and inst['@type'] == 'HowToStep':
                        steps.append(inst.get('text', ''))
            parsed['instructions'] = steps
        elif isinstance(instructions, str):
            parsed['instructions'] = [instructions]
    
    # Extract times
    if 'prepTime' in recipe_data:
        parsed['prep_time'] = recipe_data['prepTime']
    if 'cookTime' in recipe_data:
        parsed['cook_time'] = recipe_data['cookTime']
    if 'totalTime' in recipe_data and not parsed['cook_time']:
        parsed['cook_time'] = recipe_data['totalTime']
    
    # Extract servings
    if 'recipeYield' in recipe_data:
        yield_val = recipe_data['recipeYield']
        if isinstance(yield_val, list):
            parsed['servings'] = yield_val[0] if yield_val else None
        else:
            parsed['servings'] = str(yield_val)
    
    # Extract category/tags
    tags = []
    if 'recipeCategory' in recipe_data:
        cat = recipe_data['recipeCategory']
        if isinstance(cat, list):
            tags.extend(cat)
        elif cat:
            tags.append(cat)
    if 'recipeCuisine' in recipe_data:
        cuisine = recipe_data['recipeCuisine']
        if isinstance(cuisine, list):
            tags.extend(cuisine)
        elif cuisine:
            tags.append(cuisine)
    if 'keywords' in recipe_data:
        keywords = recipe_data['keywords']
        if isinstance(keywords, str):
            tags.extend([k.strip() for k in keywords.split(',')])
        elif isinstance(keywords, list):
            tags.extend(keywords)
    
    parsed['tags'] = [tag.lower() for tag in tags if tag]
    
    return parsed

def fetch_url_content(url):
    """Fetch HTML content from a URL"""
    try:
        # Create a session for better cookie handling
        session = requests.Session()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        
        response = session.get(url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()
        
        # Parse HTML and extract text
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit to first 15000 characters to stay within token limits
        return text[:15000]
    except Exception as e:
        raise Exception(f"Failed to fetch URL: {str(e)}")

def parse_recipe_with_claude(url, api_key=None):
    """Use Claude AI to parse recipe from URL, trying JSON-LD first"""
    
    # First, try to fetch the page and extract JSON-LD structured data
    html_content = None
    fetch_error = None
    
    # Try multiple header combinations
    header_variants = [
        # Variant 1: Mac Safari
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        },
        # Variant 2: Windows Chrome
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        },
        # Variant 3: Linux Firefox
        {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        }
    ]
    
    for i, headers in enumerate(header_variants):
        try:
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=20, allow_redirects=True)
            response.raise_for_status()
            html_content = response.text
            print(f"Successfully fetched URL with header variant {i+1}")
            break
        except requests.exceptions.HTTPError as e:
            fetch_error = str(e)
            if i < len(header_variants) - 1:
                print(f"Header variant {i+1} failed, trying next...")
                continue
        except Exception as e:
            fetch_error = str(e)
            if i < len(header_variants) - 1:
                continue
    
    if html_content:
        # Try to extract JSON-LD structured data first (much more reliable!)
        json_ld_recipe = extract_recipe_json_ld(html_content)
        if json_ld_recipe:
            print(f"Found JSON-LD recipe data for {url}")
            return parse_recipe_from_json_ld(json_ld_recipe, url)
        
        print(f"No JSON-LD found, falling back to Claude AI for {url}")
        
    else:
        # All fetch attempts failed
        error_msg = f"Unable to fetch URL after trying multiple methods. Last error: {fetch_error}. "
        if "403" in str(fetch_error):
            error_msg += "This website is blocking automated requests. Try: 1) Copy and paste the recipe text directly into the manual entry form, or 2) Try a different recipe URL from a more bot-friendly site (like Food Network, NYT Cooking, or Serious Eats)."
        raise Exception(error_msg)
    
    # If JSON-LD didn't work, fall back to Claude AI
    if not api_key:
        api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        raise Exception("ANTHROPIC_API_KEY not found in environment variables and JSON-LD extraction failed")
    
    # Fetch content from URL
    content = fetch_url_content(url)
    
    # Initialize Claude client
    client = Anthropic(api_key=api_key)
    
    # Create prompt for Claude
    prompt = f"""Please extract the recipe information from the following webpage content and return it as a JSON object with these exact fields:

- name: string (recipe name)
- description: string (brief description)
- ingredients: array of strings (each ingredient as a separate item)
- instructions: array of strings (each step as a separate item)
- prep_time: string (e.g., "15 minutes", null if not found)
- cook_time: string (e.g., "30 minutes", null if not found)
- servings: string (e.g., "4 servings", null if not found)
- tags: array of strings (e.g., ["dinner", "vegetarian"])

Return ONLY the JSON object, no other text. If you cannot find certain information, use null for strings and empty arrays for arrays.

Webpage content:
{content}"""

    # Call Claude API
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the response
        response_text = message.content[0].text
        
        # Parse JSON from response
        # Sometimes Claude wraps it in markdown code blocks
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        recipe_data = json.loads(response_text)
        
        # Add source URL
        recipe_data['source_url'] = url
        
        # Try to find image URL from original HTML
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for og:image meta tag
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                recipe_data['image_url'] = og_image['content']
            else:
                # Try to find first large image
                img = soup.find('img', {'class': lambda x: x and any(word in x.lower() for word in ['recipe', 'hero', 'main', 'featured'])})
                if img and img.get('src'):
                    recipe_data['image_url'] = img['src']
        except:
            pass
        
        return recipe_data
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Claude's response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Claude API error: {str(e)}")
