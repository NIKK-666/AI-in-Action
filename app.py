from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import google.generativeai as genai
from pymongo import MongoClient
from datetime import datetime
import os
import re

# Load environment variables
load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='.')

# Gemini / Gemma API Setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MongoDB Setup
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["climateDB"]
query_log = db["climateData"]
climate_data = db["gistempData"]

# Serve frontend
@app.route("/")
def serve_frontend():
    return send_from_directory('.', 'index.html')


# AI Query Handler
@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_query = request.json["query"]
        print("🔍 Received query:", user_query)

        # Extract region using simple pattern matching (expandable)
        region = None
        regions = ["California", "India", "Texas", "Australia", "Europe", "Africa"]
        for r in regions:
            if r.lower() in user_query.lower():
                region = r
                break

        # Extract year if present
        year = None
        year_match = re.search(r"\b(19|20)\d{2}\b", user_query)
        if year_match:
            year = int(year_match.group())

        # Try to enrich with MongoDB summary
        mongo_summary = None
        if region and year:
            match = climate_data.find_one({"region": region, "year": year})
            if match:
                mongo_summary = match.get("summary")

        # Prompt for AI
        if mongo_summary:
            prompt = f"""Based on the following climate data:
{mongo_summary}

Now answer this query clearly: {user_query}
"""
        else:
            prompt = f"Answer this climate question briefly and clearly: {user_query}"

        # Use the local/hosted model
        model = genai.GenerativeModel("gemma-3-12b-it")

        try:
            response = model.generate_content(prompt)
            final_answer = response.text.strip()
        except Exception as inner_error:
            print("⚠️ Falling back to 'gemini-pro':", inner_error)
            fallback_model = genai.GenerativeModel("gemini-pro")
            response = fallback_model.generate_content(prompt)
            final_answer = response.text.strip()

        # Save to MongoDB
        query_log.insert_one({
            "query": user_query,
            "region": region,
            "year": year,
            "matched_summary": mongo_summary,
            "response": final_answer,
            "timestamp": datetime.utcnow()
        })

        return jsonify({"answer": final_answer})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"answer": f"Error: {str(e)}"}), 500


# Get all query history
@app.route("/history", methods=["GET"])
def get_history():
    user_queries = list(query_log.find({}, {"_id": 0}))
    return jsonify(user_queries)


# Serve climate data to frontend map
@app.route("/climate-data", methods=["GET"])
def get_climate_data():
    try:
        data = list(climate_data.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        print("❌ Error fetching climate data:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

