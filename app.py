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

@app.route("/generate-narrative", methods=["POST"])
def generate_narrative():
    toggles = request.json.get("toggles", [])

    narrative_sections = {
        "Chief Complaint": [],
        "History": [],
        "Assessment": [],
        "Rx/Interventions": [],
        "Transport/Disposition": []
    }
    
    for item in toggles:
        label = f"Yes: {item['text']}" if item['state'] == "yes" else f"No: {item['text']}"
        narrative_sections["Assessment"].append(label)

    # Smart keyword-based sorting
    for item in toggles:
        lower_item = item.lower()
        if "complaint" in lower_item or "cc" in lower_item:
            narrative_sections["Chief Complaint"].append(item)
        elif any(kw in lower_item for kw in ["history", "pmh", "allergy", "meds"]):
            narrative_sections["History"].append(item)
        elif any(kw in lower_item for kw in ["vital", "exam", "assessment", "pain", "gcs", "symptom", "negative"]):
            narrative_sections["Assessment"].append(item)
        elif any(kw in lower_item for kw in ["administered", "given", "treatment", "intervention", "response"]):
            narrative_sections["Rx/Interventions"].append(item)
        elif any(kw in lower_item for kw in ["transport", "disposition", "care", "hospital", "refused"]):
            narrative_sections["Transport/Disposition"].append(item)
        else:
            narrative_sections["Assessment"].append(item)  # default

    # Format output
    def format_block(title, items):
        return f"{title}:\n- " + "\n- ".join(items) if items else ""

    final_narrative = "\n\n".join(
        format_block(title, items)
        for title, items in narrative_sections.items() if items
    )

    return jsonify({"narrative": final_narrative})

import os
    
if __name__ == "__main__":
     port = int(os.environ.get("PORT", 5000))
     app.run(host="0.0.0.0", port=port, debug=True)
