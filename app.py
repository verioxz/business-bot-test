from flask import Flask, request, jsonify, render_template, send_file
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote

app = Flask(__name__)

def generate_business_idea():
    ideas = [
        "Start a podcast editing service.",
        "Create an online course.",
        "Develop a mobile app.",
        "Offer freelance graphic design services.",
        "Launch an e-commerce store."
    ]
    return random.choice(ideas)

def generate_catchphrase():
    phrases = [
        "Empowering Your Future.",
        "Innovation at its Best.",
        "Dream Big, Achieve More.",
        "Your Success, Our Commitment.",
        "Where Ideas Become Reality."
    ]
    return random.choice(phrases)

def generate_logo(text="Logo"):
    # Create an image with white background
    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Define a font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Add text to the image
    d.text((10, 30), text, fill=(0, 0, 0), font=font)
    
    # Save the image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message'].lower()

    if 'business idea' in user_message:
        reply = generate_business_idea()
    elif 'catchphrase' in user_message:
        reply = generate_catchphrase()
    elif 'logo' in user_message:
        return send_file(generate_logo("Your Logo"), mimetype='image/png')
    else:
        reply = "Sorry, I can only provide business ideas, catchphrases, and logos."

    return jsonify({'reply': reply})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

