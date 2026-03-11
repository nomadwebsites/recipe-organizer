import os
import json
import requests
from anthropic import Anthropic
from bs4 import BeautifulSoup

def fetch_url_content(url):
    """Fetch HTML content from a URL"""
    try:
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
            'Cache-Control': 'max-age=0'
        }
        response = requests.get(url, headers=headers, timeout=15)
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
    """Use Claude AI to parse recipe from URL"""
    if not api_key:
        api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        raise Exception("ANTHROPIC_API_KEY not found in environment variables")
    
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
