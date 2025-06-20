# 🌍 Climate Insight Explorer

**AI-powered climate trend explorer combining real data and natural language understanding.**


---

## 🚀 Overview

**Climate Insight Explorer** helps users understand climate change by allowing them to ask simple, natural language questions like:

> “Was California hotter in 2022?”  
> “Show global warming trends from 2010–2020”

The app uses **Gemini AI / Gemma** to generate human-like responses, grounded in **real NASA GISTEMP climate data**, and visualized through a **Google Maps heatmap**.

Whether you're a student, researcher, or policymaker, this app makes climate data accessible, visual, and interactive.

---

## 🌟 Features

- 🔍 Natural language climate trend queries
- 🧠 AI-generated summaries via Gemini/Gemma
- 🗺️ Google Maps heatmap with toggleable markers and circles
- 🌡️ Interactive anomaly visualization using NASA GISTEMP data
- 🗃️ MongoDB integration for data enrichment and logging
- 📜 User query history tracking and AI response storage
- 🔐 Environment-secured API key handling with `.env`

---

## 🛠 Built With

| Category     | Technologies Used |
|--------------|-------------------|
| **Languages** | Python, JavaScript, HTML, CSS |
| **Frameworks** | Flask, Tailwind CSS |
| **AI Models** | Gemini Pro / gemma-3-12b-it |
| **APIs/Cloud** | Google Maps JavaScript API, Google Cloud, Gemini API |
| **Database** | MongoDB Atlas |
| **Frontend Libraries** | Leaflet (optional), Google Maps, Tailwind |

---

Live demo : https://ai-in-action.onrender.com

## 📦 Getting Started

### ✅ Prerequisites

- Python 3.8+
- `pip` installed
- Google API Key (for Maps + Gemini)
- MongoDB URI (from MongoDB Atlas)

### 🔧 Installation

```bash
git clone https://github.com/NIKK-666/AI-in-Action
cd climate-insight-explorer
pip install -r requirements.txt
