#!/usr/bin/env python3
"""
Daily Sales Prospecting Agent
Generates sales prospects and outreach emails using Claude
"""
import os
import json
from datetime import datetime
import requests

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

def generate_prospects():
    """Generate sales prospects using Claude API"""
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    
    prompt = """You are a sales research expert. Find 8 realistic prospects in San Antonio, Texas.
Business types to target: Accounting firms, Real estate agencies, Local tech companies, Medical offices
Company size: Small (5-50 employees)
Service offered: We automate repetitive admin tasks using AI agents, saving small businesses 15-20 hours per week
Contact email: your-email@suretek.online
For each prospect, provide EXACTLY this JSON format:
{
  "companyName": "Company Name",
  "industry": "Industry",
  "estimatedSize": "Small",
  "description": "One sentence about what they do",
  "painPoint": "Specific problem this service solves for them",
  "contactApproach": "How to find/contact them"
}
Generate exactly 8 prospects as a JSON array. Make them realistic San Antonio businesses. Return ONLY the JSON array, no markdown formatting."""
    
    data = {
        "model": "claude-opus-4-6",
        "max_tokens": 2000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        content = result['content'][0]['text']
        
        # Remove markdown code block formatting if present
        if content.startswith('```'):
            # Extract content between backticks
            parts = content.split('```')
            content = parts[1] if len(parts) > 1 else content
            # Remove 'json' label if present
            if content.startswith('json'):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON from response
        prospects = json.loads(content)
        
        # Save results
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = {
            "generated_at": timestamp,
            "prospects": prospects
        }
        
        # Save to JSON file
        output_file = f"prospects_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Generated {len(prospects)} prospects")
        print(f"📝 Saved to {output_file}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"Response was: {content}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        exit(1)

if __name__ == "__main__":
    generate_prospects()
