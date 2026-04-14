import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Replace with your actual key - Keep it in quotes
GEMINI_KEY = "AIzaSyDckA2C5hCmEQNFGpyt0piXFo2DseshCPI" # Put your key back here privately

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
    data = request.json
    ad_text = data.get('ad', '').strip()
    url = data.get('url', '').strip()

    if not ad_text:
        return jsonify({"status": "error", "message": "Ad text is required"})

    prompt = f"""
    You are a Conversion Rate Optimization (CRO) expert.
    User Ad Creative text: "{ad_text}"
    Current Landing Page URL: "{url}"
    
    Task: Create a professional HTML <div> to be used as a personalized overlay card.
    Requirements:
    1. Matching headline that connects to the ad.
    2. Benefit-driven subheadline.
    3. Clear Call to Action (CTA) button.
    4. Use inline CSS for a modern, clean look (shadows, rounded corners).
    
    Return ONLY the HTML <div>. No markdown backticks.
    """

    try:
        response = model.generate_content(prompt)
        # Clean markdown in case the model adds it anyway
        clean_html = response.text.replace("```html", "").replace("```", "").strip()
        
        return jsonify({"status": "success", "rewritten": clean_html})

    except Exception as e:
        print(f"API Error: {e}")
        fallback_html = f"""
        <div style="padding:20px; background:white; border-radius:10px; border-left:5px solid #2a5298; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h2 style="color:#2a5298;">🚀 Special Offer: {ad_text}</h2>
            <p>We've personalized this experience based on your interest.</p>
            <button style="background:#2a5298; color:white; padding:10px 15px; border:none; border-radius:5px;">Claim Now</button>
        </div>
        """
        return jsonify({"status": "success", "rewritten": fallback_html})

if __name__ == '__main__':
    app.run(debug=True)