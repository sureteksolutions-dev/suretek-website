#!/usr/bin/env python3
"""
Daily Sales Prospecting Agent
Generates sales prospects and sends them via email
"""
import os
import json
from datetime import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
RECIPIENT_EMAIL = 'sureteksolutions@gmail.com'

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
            parts = content.split('```')
            content = parts[1] if len(parts) > 1 else content
            if content.startswith('json'):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON from response
        prospects = json.loads(content)
        return prospects
        
    except Exception as e:
        print(f"❌ Error generating prospects: {e}")
        exit(1)

def send_email(prospects):
    """Send prospects via email"""
    try:
        # Create email
        msg = MIMEMultipart('html')
        msg['From'] = RECIPIENT_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Daily Sales Prospects - {datetime.now().strftime('%B %d, %Y')}"
        
        # Build HTML email body
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
                .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .prospect {{ background-color: white; padding: 20px; margin-bottom: 15px; border-left: 4px solid #3498db; border-radius: 3px; }}
                .prospect h3 {{ color: #2c3e50; margin-top: 0; }}
                .prospect-meta {{ color: #7f8c8d; font-size: 13px; margin: 10px 0; }}
                .prospect-detail {{ margin: 10px 0; }}
                .prospect-detail strong {{ color: #2c3e50; }}
                .footer {{ text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 Daily Sales Prospects</h1>
                    <p>Your AI-powered sales intelligence for {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                <p>Hello! Here are your 8 qualified prospects for today:</p>
        """
        
        for i, prospect in enumerate(prospects, 1):
            html += f"""
                <div class="prospect">
                    <h3>#{i} - {prospect['companyName']}</h3>
                    <div class="prospect-meta">
                        <strong>Industry:</strong> {prospect['industry']} | 
                        <strong>Size:</strong> {prospect['estimatedSize']}
                    </div>
                    <div class="prospect-detail">
                        <strong>What they do:</strong> {prospect['description']}
                    </div>
                    <div class="prospect-detail">
                        <strong>Their pain point:</strong> {prospect['painPoint']}
                    </div>
                    <div class="prospect-detail">
                        <strong>How to contact:</strong> {prospect['contactApproach']}
                    </div>
                </div>
            """
        
        html += """
                <div class="footer">
                    <p>Generated by Suretek Sales Prospecting Agent</p>
                    <p>Powered by Claude AI</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Send email via Gmail
        print(f"📧 Sending email to {RECIPIENT_EMAIL}...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(RECIPIENT_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Generating sales prospects...")
    prospects = generate_prospects()
    print(f"✅ Generated {len(prospects)} prospects")
    
    print("📧 Sending email...")
    send_email(prospects)
