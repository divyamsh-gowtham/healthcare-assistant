from fastapi import FastAPI, UploadFile, File
from prescription import extract_text, explain_prescription
import os

app = FastAPI()

@app.post("/upload")

async def upload_prescription(file: UploadFile = File(...)):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)

    explanation = explain_prescription(text)

    return {
        "extracted_text": text,
        "ai_explanation": explanation
    }