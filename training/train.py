import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification

# --------------------
# Dataset
# --------------------
class FakeNewsDataset(Dataset):
    def __init__(self, csv_path, tokenizer, max_len=256):
        self.data = pd.read_csv(csv_path)
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = str(self.data.iloc[idx]["text"])
        label = int(self.data.iloc[idx]["label"])

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(label)
        }

# --------------------
# Load tokenizer + model
# --------------------
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# --------------------
# Load data
# --------------------
dataset = FakeNewsDataset("../data/train.csv", tokenizer)
loader = DataLoader(dataset, batch_size=8, shuffle=True)

# --------------------
# Training setup
# --------------------
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# --------------------
# Training loop
# --------------------
model.train()
for epoch in range(2):
    print(f"Epoch {epoch+1}")
    for batch in loader:
        optimizer.zero_grad()

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        loss.backward()
        optimizer.step()

    print("Loss:", loss.item())

# --------------------
# Save trained model
# --------------------
torch.save(model.state_dict(), "../backend/model/model.pt")
print("Training finished, model saved.")
