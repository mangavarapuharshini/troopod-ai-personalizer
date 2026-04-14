import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# API Key setup - Use environment variable for security or paste here for testing
GEMINI_KEY = "AIzaSyDckA2C5hCmEQNFGpyt0piXFo2DseshCPI" 

try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Configuration Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Supports both JSON (for API testing) and Form (for browser)
    if request.is_json:
        data = request.json
    else:
        data = request.form

    # Variables link directly to index.html name attributes
    ad_text = data.get('interest') or data.get('ad') or ""
    ad_text = ad_text.strip()
    url = data.get('url', '').strip()

    if not ad_text:
        return render_template('index.html', error="Please enter your interest.")

    prompt = f"""
    You are a Conversion Rate Optimization (CRO) expert.
    User Interest: "{ad_text}"
    Target URL: "{url}"
    
    Task: Create a professional HTML <div> to be used as a personalized overlay card.
    Requirements:
    1. Catchy headline related to {ad_text}.
    2. Benefit-driven subheadline.
    3. A professional Call to Action (CTA) button.
    4. Use inline CSS for a modern look (shadows, rounded corners).
    
    Return ONLY the HTML <div>. No markdown backticks.
    """

    try:
        response = model.generate_content(prompt)
        clean_html = response.text.replace("```html", "").replace("```", "").strip()
        
        return render_template('index.html', 
                               personalized_content=clean_html, 
                               target_url=url, 
                               interest=ad_text)

    except Exception as e:
        print(f"API Error: {e}")
        fallback_html = f"""
        <div style="padding:20px; background:white; border-radius:10px; border-left:5px solid #2563eb; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h2 style="color:#2563eb; margin-top:0;">🚀 Special Offer for {ad_text}</h2>
            <p>We've personalized this experience just for you.</p>
            <button style="background:#2563eb; color:white; padding:10px 15px; border:none; border-radius:5px; cursor:pointer;">Claim Now</button>
        </div>
        """
        return render_template('index.html', 
                               personalized_content=fallback_html, 
                               target_url=url, 
                               interest=ad_text)

if __name__ == '__main__':
    app.run(debug=True)
