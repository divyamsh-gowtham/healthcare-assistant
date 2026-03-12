import pytesseract
from PIL import Image
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_text(image_path):

    img = Image.open(image_path)

    text = pytesseract.image_to_string(img)

    return text


def explain_prescription(text):

    prompt = f"""
You are a healthcare assistant.

Explain this prescription in simple terms.

Extract:
- medicines
- dosage
- duration
- purpose

Prescription:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content