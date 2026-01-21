from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# -----------------------------
# CONFIG
# -----------------------------
MODEL_PATH = "../training/model.pt"  # path to your trained model
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# FASTAPI INIT
# -----------------------------
app = FastAPI(title="Fake News Detection API")

# -----------------------------
# REQUEST BODY MODEL
# -----------------------------
class NewsRequest(BaseModel):
    text: str

# -----------------------------
# LOAD MODEL & TOKENIZER
# -----------------------------
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Load the trained model
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=2
)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()

# -----------------------------
# PREDICTION ROUTE
# -----------------------------
@app.post("/predict")
def predict(news: NewsRequest):
    if not news.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    # Tokenize input
    inputs = tokenizer(
        news.text,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # Model inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1)[0].cpu().numpy()

    # Map prediction
    labels = ["REAL", "FAKE"]
    prediction_idx = int(probs.argmax())
    prediction = labels[prediction_idx]
    confidence = float(probs[prediction_idx]) * 100

    # Return result
    return {
        "prediction": prediction,
        "confidence": confidence,
        "probabilities": {
            "real": float(probs[0] * 100),
            "fake": float(probs[1] * 100)
        },
        "features": {
            "word_count": len(news.text.split()),
            "has_quotes": '"' in news.text or "'" in news.text,
            "has_dates": any(month in news.text.lower() for month in [
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"
            ])
        }
    }

# -----------------------------
# HEALTHCHECK
# -----------------------------
@app.get("/")
def root():
    return {"message": "Fake News Detection API is running!"}
