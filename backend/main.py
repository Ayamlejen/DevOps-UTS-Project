import json
import os
import tempfile
from pathlib import Path

import torch
import torch.nn.functional as F

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import SessionLocal
from db_models import PredictionHistory

from models.cnn_model import MusicGenreCNN
from models.preprocessing import audio_to_melspectrogram


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "music_genre_cnn.pth"
CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"
CONFIG_PATH = MODEL_DIR / "model_config.json"

DEVICE = torch.device("cpu")


with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

if isinstance(class_names, dict):
    class_names = config["classes"]


model = MusicGenreCNN(num_classes=len(class_names))

state_dict = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=True
)

model.load_state_dict(state_dict)
model.to(DEVICE)
model.eval()

print("Model CNN berhasil dimuat!")


app = FastAPI(
    title="Music Genre Classification API",
    description="API klasifikasi genre musik menggunakan CNN",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Music Genre Classification API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "backend",
        "model": "loaded"
    }


@app.post("/predict")
async def predict_genre(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="File harus berformat WAV."
        )

    temp_path = None
    db = SessionLocal()

    try:
        audio_bytes = await file.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="File audio kosong."
            )

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        input_tensor = audio_to_melspectrogram(
            temp_path,
            sample_rate=config["sample_rate"],
            duration=config["duration"],
            n_mels=config["n_mels"],
            n_fft=config["n_fft"],
            hop_length=config["hop_length"],
            target_height=config["target_height"],
            target_width=config["target_width"]
        )

        input_tensor = input_tensor.unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)

            confidence, predicted_index = torch.max(
                probabilities, dim=1
            )

        predicted_genre = class_names[predicted_index.item()]
        confidence_value = confidence.item()

        history = PredictionHistory(
            filename=Path(file.filename).name,
            predicted_genre=predicted_genre,
            confidence=confidence_value
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        return {
            "message": "Prediksi berhasil",
            "filename": Path(file.filename).name,
            "predicted_genre": predicted_genre,
            "confidence": round(confidence_value, 4),
            "confidence_percentage": round(
                confidence_value * 100, 2
            ),
            "history_id": history.id
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan: {str(e)}"
        )

    finally:
        db.close()

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)