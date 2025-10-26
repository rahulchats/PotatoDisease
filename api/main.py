from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# --- Load Model ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../saved_models/1")
MODEL_PATH = os.path.abspath(MODEL_PATH)
MODEL = tf.keras.models.load_model(MODEL_PATH)
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

# --- Mount client folder as static ---
CLIENT_PATH = os.path.join(os.path.dirname(__file__), "../client")
app.mount("/client", StaticFiles(directory=CLIENT_PATH), name="client")

# --- Serve HTML ---
@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(CLIENT_PATH, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

# --- Health Check ---
@app.get("/ping")
async def ping():
    return {"message": "Server is alive!"}

# --- Utility ---
def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

# --- Prediction Endpoint ---
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        "class": predicted_class,
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
