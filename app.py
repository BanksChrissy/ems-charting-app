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
    data = request.json
    toggles = data.get("toggles", [])

    # Combine structured inputs into toggle-like strings for classification
    extra_inputs = []
    if data.get("chief"):
        extra_inputs.append(f"Chief Complaint: {data['chief']}")
    if data.get("pmh"):
        extra_inputs.append(f"PMH: {data['pmh']}")
    if data.get("meds"):
        extra_inputs.append(f"Medications: {data['meds']}")
    if data.get("allergies"):
        extra_inputs.append(f"Allergies: {data['allergies']}")
    if data.get("interventions"):
        extra_inputs.append(f"Intervention: {data['interventions']}")
    if data.get("disposition"):
        extra_inputs.append(f"Disposition: {data['disposition']}")

    all_items = extra_inputs + toggles

    narrative_sections = {
        "Chief Complaint": [],
        "History": [],
        "Assessment": [],
        "Rx/Interventions": [],
        "Transport/Disposition": []
    }

    for item in all_items:
        lower_item = item.lower()
        if "chief complaint" in lower_item or "cc:" in lower_item:
            narrative_sections["Chief Complaint"].append(item)
        elif any(kw in lower_item for kw in ["history", "pmh", "allergy", "meds"]):
            narrative_sections["History"].append(item)
        elif any(kw in lower_item for kw in ["vital", "exam", "assessment", "pain", "gcs", "symptom", "negative", "[+]", "[-]", "yes:", "no:"]):
            narrative_sections["Assessment"].append(item)
        elif any(kw in lower_item for kw in ["administered", "given", "treatment", "intervention", "response"]):
            narrative_sections["Rx/Interventions"].append(item)
        elif any(kw in lower_item for kw in ["transport", "disposition", "care", "hospital", "refused"]):
            narrative_sections["Transport/Disposition"].append(item)
        else:
            narrative_sections["Assessment"].append(item)  # fallback

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
