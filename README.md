# 📰 Fake News Detection System (ML + Full Stack)

A complete **Machine Learning–powered Fake News Detection system** using  
**BERT**, **FastAPI**, and **React (Vite)**.

This project includes:
- Dataset-based ML training
- Model inference API
- Frontend UI
- Proper ML project structure

---

## 🚀 Features

- 🔍 Detects whether news text is **Fake** or **Real**
- 🧠 Trained using **BERT (bert-base-uncased)**
- ⚙️ Backend API built with **FastAPI**
- 🖥️ Frontend built with **React + Vite**
- 📦 Clean GitHub repo (model weights ignored)

---

## 🗂️ Project Structure


FakeNewsDetection/
│
├── backend/
│ ├── app.py # FastAPI inference server
│ └── model/ # Saved trained model (ignored in git)
│
├── frontend/
│ ├── src/
│ │ └── FakeNewsDetector.tsx
│ └── package.json
│
├── training/
│ └── train.py # Model training script
│
├── README.md
└── .gitignore


---

## 🧠 Machine Learning Details

- **Model:** BERT (bert-base-uncased)
- **Task:** Binary text classification (Fake / Real)
- **Framework:** PyTorch + HuggingFace Transformers
- **Training:** Custom dataset used inside `train.py`
- **Output:** `model.pt` (ignored from GitHub)

---

## 🏋️ Training the Model

```bash
cd training
python train.py
