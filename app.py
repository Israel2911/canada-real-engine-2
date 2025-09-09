from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing for all domains
CORS(app)

@app.route("/")
def index():
    """A simple health-check endpoint to confirm the API is running."""
    return "✅ REAL Engine API is live"

@app.route("/data")
def get_data():
    """Serves the latest data from the JSON file."""
    file_path = os.path.abspath("real-engine-data.json")
    print(f"🧾 Serving file from: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: Data file not found at {file_path}")
        return jsonify({"error": "Data file not found. The data generation process may not have run yet."}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return jsonify(data)
    except json.JSONDecodeError:
        print(f"❌ Error: Could not decode JSON from {file_path}. The file may be empty or corrupted.")
        return jsonify({"error": "Failed to read data file. It may be temporarily unavailable."}), 500

if __name__ == "__main__":
    # The application runs on the port provided by the hosting environment (e.g., Render) or defaults to 10000.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
