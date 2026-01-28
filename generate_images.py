import json
import base64
import requests
import time
from PIL import Image, ImageDraw
import random
import math
import os

API_KEY = "AIzaSyDVQqm4N-TufAv-4c8rRA1NjPE6W9lY9pA"
BASE_PATH = "/Users/abdulazim/webapps/zehnly-subs/gamified_learning/data"

# Category prompts - cute kawaii icons for each topic
CATEGORIES = {
    "02_food_and_drinks": "Cute cartoon hamburger and french fries icon for mobile game. Round badge shape. Happy smiling food. Soft gradients, vibrant colors. Clean white background. Kawaii style, high quality game asset.",
    "03_family_and_people": "Cute cartoon family icon - mom dad and child holding hands. Round badge shape. Happy smiling faces. Soft gradients, warm colors. Clean white background. Kawaii style, high quality game asset.",
    "04_body_parts": "Cute cartoon red heart with a happy face icon for mobile game. Round badge shape. Soft gradients, red and pink colors. Clean white background. Kawaii style, high quality game asset.",
    "05_colors": "Cute cartoon paint palette with colorful dots icon for mobile game. Round badge shape. Rainbow colors, happy face. Soft gradients. Clean white background. Kawaii style, high quality game asset.",
    "06_numbers_and_time": "Cute cartoon clock with numbers 123 icon for mobile game. Round badge shape. Happy smiling face. Soft gradients, blue and gold colors. Clean white background. Kawaii style, high quality game asset.",
    "07_house_and_furniture": "Cute cartoon house with chimney icon for mobile game. Round badge shape. Happy cozy home. Soft gradients, warm colors orange and brown. Clean white background. Kawaii style, high quality game asset.",
    "08_clothes_and_accessories": "Cute cartoon t-shirt and hat icon for mobile game. Round badge shape. Happy colorful clothes. Soft gradients, purple and blue colors. Clean white background. Kawaii style, high quality game asset.",
    "09_weather_and_nature": "Cute cartoon sun with clouds icon for mobile game. Round badge shape. Happy smiling sun face. Soft gradients, yellow and blue colors. Clean white background. Kawaii style, high quality game asset.",
    "10_transportation": "Cute cartoon red car icon for mobile game. Round badge shape. Happy smiling car face. Soft gradients, red and blue colors. Clean white background. Kawaii style, high quality game asset.",
    "11_school_and_education": "Cute cartoon book and pencil icon for mobile game. Round badge shape. Happy school supplies. Soft gradients, blue and yellow colors. Clean white background. Kawaii style, high quality game asset.",
    "12_sports_and_games": "Cute cartoon soccer ball icon for mobile game. Round badge shape. Happy smiling ball face. Soft gradients, black white and green colors. Clean white background. Kawaii style, high quality game asset.",
    "13_technology": "Cute cartoon laptop computer icon for mobile game. Round badge shape. Happy smiling screen face. Soft gradients, blue and silver colors. Clean white background. Kawaii style, high quality game asset.",
    "14_work_and_office": "Cute cartoon briefcase icon for mobile game. Round badge shape. Happy professional look. Soft gradients, brown and gold colors. Clean white background. Kawaii style, high quality game asset.",
    "15_health_and_medicine": "Cute cartoon doctor with stethoscope icon for mobile game. Round badge shape. Happy friendly doctor. Soft gradients, white and blue colors. Clean white background. Kawaii style, high quality game asset.",
    "16_emotions_and_feelings": "Cute cartoon happy yellow smiley face icon for mobile game. Round badge shape. Big smile, rosy cheeks. Soft gradients, yellow and pink colors. Clean white background. Kawaii style, high quality game asset.",
    "17_actions_and_verbs": "Cute cartoon running shoes with motion lines icon for mobile game. Round badge shape. Energetic and fast. Soft gradients, red and white colors. Clean white background. Kawaii style, high quality game asset.",
    "18_places_and_locations": "Cute cartoon city buildings and trees icon for mobile game. Round badge shape. Happy colorful town. Soft gradients, multiple colors. Clean white background. Kawaii style, high quality game asset.",
    "19_kitchen_and_cooking": "Cute cartoon chef hat and cooking pot icon for mobile game. Round badge shape. Happy cooking theme. Soft gradients, white and red colors. Clean white background. Kawaii style, high quality game asset.",
    "20_music_and_entertainment": "Cute cartoon music notes and headphones icon for mobile game. Round badge shape. Happy musical theme. Soft gradients, purple and pink colors. Clean white background. Kawaii style, high quality game asset.",
}

def generate_base_image(prompt, output_path):
    """Generate base image using Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "responseModalities": ["image", "text"]
        }
    }

    response = requests.post(url, json=payload, timeout=120)
    data = response.json()

    if 'candidates' in data:
        img_data = data['candidates'][0]['content']['parts'][1]['inlineData']['data']
        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(img_data))
        return True
    return False

def remove_background(img):
    """Remove white/near-white background"""
    pixels = list(img.getdata())
    new_data = []
    for p in pixels:
        r, g, b, a = p
        if r > 245 and g > 245 and b > 245:
            new_data.append((0, 0, 0, 0))
        elif r < 10 and g < 10 and b < 10:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(p)
    img.putdata(new_data)
    return img

def create_locked(img):
    """Create grayscale locked version"""
    gray = img.convert('LA').convert('RGBA')
    orig_pixels = list(img.getdata())
    gray_pixels = list(gray.getdata())

    locked_data = []
    for i, p in enumerate(gray_pixels):
        if orig_pixels[i][3] == 0:
            locked_data.append((0, 0, 0, 0))
        else:
            locked_data.append(p)

    result = Image.new('RGBA', img.size)
    result.putdata(locked_data)
    return result

def create_damaged(img):
    """Create damaged version with cracks"""
    width, height = img.size

    # Color shift
    pixels = list(img.getdata())
    damaged_data = []
    for p in pixels:
        r, g, b, a = p
        if a == 0:
            damaged_data.append((0, 0, 0, 0))
        else:
            new_r = min(255, int(r * 0.75 + 50))
            new_g = min(255, int(g * 0.55 + 25))
            new_b = min(255, int(b * 0.4 + 10))
            damaged_data.append((new_r, new_g, new_b, a))

    damaged = Image.new('RGBA', (width, height))
    damaged.putdata(damaged_data)

    # Add cracks
    crack_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(crack_layer)

    random.seed(42)
    crack_dark = (25, 18, 12, 255)
    crack_light = (80, 60, 40, 180)
    center_x, center_y = width // 2, height // 2

    for angle_deg in [30, 100, 160, 220, 310]:
        angle = math.radians(angle_deg + random.randint(-15, 15))
        pts = []
        cx, cy = center_x + random.randint(-20, 20), center_y + random.randint(-20, 20)
        pts.append((cx, cy))

        for i in range(5):
            step = random.randint(25, 45)
            cx += int(math.cos(angle) * step + random.randint(-12, 12))
            cy += int(math.sin(angle) * step + random.randint(-12, 12))
            pts.append((cx, cy))

        draw.line(pts, fill=crack_light, width=6)
        draw.line(pts, fill=crack_dark, width=3)

        if len(pts) > 2:
            for bi in [1, 3]:
                if bi < len(pts):
                    bx, by = pts[bi]
                    branch_angle = angle + random.choice([-0.7, 0.7])
                    bpts = [(bx, by)]
                    for j in range(3):
                        bx += int(math.cos(branch_angle) * 20)
                        by += int(math.sin(branch_angle) * 20)
                        bpts.append((bx, by))
                    draw.line(bpts, fill=crack_dark, width=2)

    # Mask cracks to image area
    orig_alpha = img.split()[3]
    crack_r, crack_g, crack_b, crack_a = crack_layer.split()

    orig_alpha_data = list(orig_alpha.getdata())
    crack_alpha_data = list(crack_a.getdata())
    new_alpha_data = []
    for i in range(len(orig_alpha_data)):
        if orig_alpha_data[i] > 0 and crack_alpha_data[i] > 0:
            new_alpha_data.append(crack_alpha_data[i])
        else:
            new_alpha_data.append(0)

    new_crack_alpha = Image.new('L', (width, height))
    new_crack_alpha.putdata(new_alpha_data)
    crack_layer = Image.merge('RGBA', (crack_r, crack_g, crack_b, new_crack_alpha))

    return Image.alpha_composite(damaged, crack_layer)

def process_category(folder, prompt):
    """Generate and process images for one category"""
    img_path = f"{BASE_PATH}/{folder}/images"
    temp_path = f"{img_path}/temp_base.png"

    print(f"Generating {folder}...")

    # Generate base
    if not generate_base_image(prompt, temp_path):
        print(f"  Failed to generate {folder}")
        return False

    # Process
    img = Image.open(temp_path).convert('RGBA')
    img = remove_background(img)

    # Save 3 states
    img.save(f"{img_path}/active.png")
    create_locked(img).save(f"{img_path}/locked.png")
    create_damaged(img).save(f"{img_path}/damaged.png")

    # Cleanup
    os.remove(temp_path)

    print(f"  Done: {folder}")
    return True

if __name__ == "__main__":
    for folder, prompt in CATEGORIES.items():
        success = process_category(folder, prompt)
        if success:
            time.sleep(2)  # Rate limit
        else:
            time.sleep(5)

    print("\nAll done!")
