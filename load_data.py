import csv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os

# MongoDB setup
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["climateDB"]
collection = db["gistemp"]
collection.delete_many({})  # Optional: clear old data

# AI Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load CSV (Assuming file: GLB.Ts+dSST.csv)
with open("GLB.Ts+dSST.csv", "r") as file:
    reader = csv.reader(file)
    rows = list(reader)

# Skip header rows
data_rows = rows[7:]

for row in data_rows:
    if len(row) < 13 or not row[0].isdigit():
        continue

    year = row[0]
    monthly_anomalies = row[1:13]

    try:
        monthly_anomalies = [float(x) if x.strip() != "***" else None for x in monthly_anomalies]
        annual_avg = sum(filter(None, monthly_anomalies)) / len([x for x in monthly_anomalies if x is not None])
    except:
        continue

    summary = f"In {year}, the global temperature anomaly was approximately {annual_avg:.2f}°C relative to 1951–1980 average."
    embedding = model.encode(summary).tolist()

    collection.insert_one({
        "year": int(year),
        "monthly_anomalies": monthly_anomalies,
        "annual_avg": annual_avg,
        "summary": summary,
        "vector": embedding
    })

print("✅ GISTEMP data loaded into MongoDB.")
