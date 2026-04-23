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
        "x-api-key": ANTHROPIC_API_KEY
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

Generate exactly 8 prospects as a JSON array. Make them realistic San Antonio businesses. Return ONLY valid JSON array."""

    data = {
        "model": "claude-opus-4-20250805",
        "max_tokens": 2000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    result = response.json()
    content = result['content'][0]['text']
    
    # Parse JSON from response
    prospects = json.loads(content)
    
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = {
        "generated_at": timestamp,
        "prospects": prospects
    }
    
    # Save to CSV-like format for easy reading
    output_file = f"prospects_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Generated {len(prospects)} prospects")
    print(f"📁 Saved to {output_file}")

if __name__ == "__main__":
    try:
        generate_prospects()
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
