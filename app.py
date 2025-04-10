from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Example route for toggles
@app.route("/")
def index():
    return render_template("index.html")

# Placeholder: Load pertinent negatives (would normally come from DB)
@app.route("/pertinent-negatives/<protocol>")
def get_negatives(protocol):
    negatives = {
        "bradycardia": [
            "No altered mental status",
            "No hypotension",
            "No chest pain",
            "No signs of shock"
        ]
    }
    return jsonify(negatives.get(protocol.lower(), []))

# Placeholder for narrative generation
@app.route("/generate-narrative", methods=["POST"])
def generate_narrative():
    toggles = request.json.get("toggles", [])
    narrative = "Patient assessment includes: " + ", ".join(toggles)
    return jsonify({"narrative": narrative})

import os
    
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=True)
