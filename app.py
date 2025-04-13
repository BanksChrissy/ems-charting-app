from flask import Flask, render_template, request, jsonify
import psycopg2
import json

app = Flask(__name__)

with open("pertinent_negatives.json") as f:
    all_negatives = json.load(f)

# Example route for toggles
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pertinent-negatives", methods=["POST"])
def get_negatives():
    requested = request.json.get("protocols", [])
    response = {}

    for protocol in requested:
        if protocol in all_negatives:
            response[protocol] = all_negatives[protocol]

    return jsonify(response)
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
