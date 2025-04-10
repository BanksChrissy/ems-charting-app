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
    "adult---bradycardia": [
        "No altered mental status",
        "No hypotension",
        "No chest pain",
        "No signs of shock",
        "No acute CHF",
        "No seizure activity",
        "No syncope",
        "No respiratory distress",
        "No pacemaker failure",
        "No signs of MI",
        "No drug overdose",
        "No hyperkalemia indicators",
        "No hypoxia",
        "No hypothermia",
        "No signs of elevated ICP or stroke",
        "No bradycardia-induced instability",
        "No history of heart transplant",
        "No AV blocks seen on ECG",
        "No beta-blocker or calcium channel blocker use",
        "No pacing required",
        "No Atropine administered",
        "No push-dose epinephrine given"
    ],
    "adult---general-adult-trauma-assessment": [
        "No altered mental status",
        "No hypotension or shock",
        "No pain or deformities",
        "No active bleeding",
        "No tension pneumothorax",
        "No sucking chest wound",
        "No obvious fractures",
        "No signs of traumatic brain injury",
        "No open wounds",
        "No abnormal GCS",
        "No need for airway intervention",
        "No pulse oximetry <94%",
        "No capnography abnormalities",
        "No multisystem trauma"
    ],
    "adult---abdominal-pain-flank-pain-nausea-vomiting": [
        "No nausea or vomiting",
        "No tenderness or pain on abdominal exam",
        "No diarrhea or constipation",
        "No vaginal bleeding or discharge",
        "No urinary complaints",
        "No signs of shock",
        "No fever",
        "No pregnancy suspected",
        "No cardiac etiology suspected",
        "No surgical history relevant to pain",
        "No antiemetics administered",
        "No pain medication administered"
    ],
    "adult---behavioral-emergencies": [
        "No suicidal ideation",
        "No homicidal ideation",
        "No hallucinations or delusions",
        "No bizarre or violent behavior",
        "No recent trauma or overdose suspected",
        "No psychiatric history",
        "No hypoxia, hypoglycemia, or electrolyte disturbances suspected",
        "No restraints used",
        "No sedation administered",
        "No combative or aggressive behavior",
        "No law enforcement intervention required"
    ],
    "adult---burns": [
        "No thermal, chemical, or electrical burns observed",
        "No inhalational injury suspected",
        "No facial burns or airway compromise",
        "No signs of shock or hypotension",
        "No significant pain reported",
        "No >20% BSA burns",
        "No circumferential burns",
        "No hoarseness or voice changes",
        "No need for fluid resuscitation",
        "No indication for early intubation",
        "No pain management required"
    ],
    "adult---cardiac-arrest-non-traumatic": [
        "No signs of unresponsiveness",
        "No apneic episodes",
        "No pulselessness detected",
        "No DNR or POLST present",
        "No signs of hypoxia",
        "No shockable rhythm on monitor",
        "No medications administered",
        "No reversible causes found (H’s & T’s)",
        "No need for mechanical CPR",
        "No airway management required",
        "No rhythm changes during CPR"
    ],
    "adult---chest-pain-non-traumatic-and-suspected-acute-coronary-syndrome": [
        "No chest pain or pressure",
        "No radiation of pain",
        "No diaphoresis or pallor",
        "No shortness of breath",
        "No nausea or dizziness",
        "No hypotension or abnormal vitals",
        "No recent use of erectile dysfunction meds",
        "No signs of right ventricular infarction",
        "No contraindications to nitroglycerin",
        "No indication for 12-lead ECG",
        "No STEMI identified on ECG"
    ],
    "adult---childbirth-labor": [
        "No signs of crowning",
        "No contractions reported",
        "No vaginal bleeding or discharge",
        "No fetal movement detected",
        "No abnormal fetal presentation",
        "No meconium noted",
        "No signs of placenta previa or cord prolapse",
        "No APGAR scores outside normal range",
        "No complications requiring resuscitation"
    ],
    "adult---cold-related-illness": [
        "No AMS or confusion",
        "No shivering or cold extremities",
        "No bradycardia or hypotension",
        "No exposure to cold environment",
        "No need for warming measures",
        "No signs of systemic hypothermia",
        "No abnormal body temperature",
        "No signs of frostbite or localized cold injury",
        "No underlying conditions contributing"
    ],
    "adult---epistaxis": [
        "No nasal bleeding present",
        "No trauma to the face or nose",
        "No posterior oropharyngeal bleeding",
        "No anticoagulant or antiplatelet use",
        "No hypertension history",
        "No signs of blood in vomitus",
        "No nasal sprays administered",
        "No active suction required",
        "No clotting disorder suspected"
    ],
    "adult---heat-related-illness": [
        "No exposure to hot environments",
        "No altered mental status",
        "No signs of dehydration",
        "No hot, dry skin or temperature >104°F",
        "No hypotension or shock",
        "No seizures or nausea",
        "No exertion history",
        "No passive or active cooling needed",
        "No signs of heat stroke or exhaustion"
    ],
    "adult---hyperkalemia-suspected": [
        "No history of renal failure or dialysis",
        "No bradycardia, peaked T-waves, or widened QRS on ECG",
        "No cardiac conduction disturbances",
        "No signs of weakness or abdominal symptoms",
        "No trauma or crush injury history",
        "No hyperkalemia-specific medications given"
    ],
    "adult---obstetrical-emergency": [
        "No history of pre-eclampsia or eclampsia",
        "No seizures during pregnancy",
        "No hypertension or severe headache",
        "No vision changes or RUQ pain",
        "No vaginal bleeding or edema of hands/face",
        "No recent childbirth or postpartum symptoms",
        "No abnormal vital signs during pregnancy"
    ],
    "adult---overdose-poisoning": [
        "No suspected ingestion or exposure to toxins",
        "No altered mental status",
        "No abnormal respiratory rate or hypotension",
        "No seizure activity",
        "No signs of SLUDGE symptoms",
        "No evidence of specific OD (TCA, ASA, etc.)",
        "No Naloxone or antidotes administered"
    ],
    "adult---pain-management": [
        "No pain reported or rated 0/10",
        "No signs of trauma or discomfort on exam",
        "No indication for analgesic medications",
        "No nausea or vomiting post-medication",
        "No significant BP or respiratory changes",
        "No allergies to analgesics",
        "No patient refusal of pain management"
    ],
    "adult---pulmonary-edema-chf": [
        "No respiratory distress or rales",
        "No orthopnea or JVD",
        "No pink, frothy sputum",
        "No peripheral edema",
        "No hypotension or shock",
        "No history of CHF",
        "No nitroglycerin administration",
        "No contraindications to nitroglycerin",
        "No evidence of MI"
    ],
    "adult---respiratory-distress": [
        "No shortness of breath or dyspnea",
        "No wheezing or rhonchi",
        "No stridor or use of accessory muscles",
        "No history of asthma or COPD",
        "No fever or productive cough",
        "No exposure to inhaled toxins",
        "No signs of pneumonia",
        "No abnormal ETCO2",
        "No need for nebulizer treatments"
    ],
    "adult---seizure": [
        "No witnessed seizure activity",
        "No incontinence or oral trauma",
        "No seizure history",
        "No abnormal mental status",
        "No signs of post-ictal state",
        "No abnormal blood glucose",
        "No trauma or pregnancy-related cause",
        "No benzodiazepines administered"
    ],
    "adult---sepsis": [
        "No history of recent infection or fever",
        "No altered mental status",
        "No abnormal vital signs (temp, HR, RR, BP)",
        "No delayed capillary refill",
        "No ETCO2 <25",
        "No recent hospitalizations or surgery",
        "No need for IV fluid bolus",
        "No signs of pulmonary edema",
        "No need for vasopressors"
    ],
    "adult---shock": [
        "No hypotension or poor perfusion",
        "No altered mental status",
        "No tachycardia",
        "No signs of bleeding or trauma",
        "No fever or suspected sepsis",
        "No signs of anaphylaxis or cardiac etiology",
        "No delayed cap refill",
        "No ETCO2 <25",
        "No need for vasopressors or fluid resuscitation"
    ],
    "adult---smoke-inhalation": [
        "No smoke exposure history",
        "No facial burns or singed nasal hairs",
        "No shortness of breath",
        "No stridor or wheezing",
        "No altered mental status",
        "No hoarseness or voice changes",
        "No signs of airway compromise",
        "No carbon monoxide poisoning suspected"
    ],
    "adult---stemi-suspected": [
        "No chest pain or pressure",
        "No radiation to jaw/arm/neck",
        "No diaphoresis or pallor",
        "No shortness of breath",
        "No recent use of ED medications",
        "No hypotension or bradycardia",
        "No signs of inferior wall infarction",
        "No 12-lead ECG changes",
        "No STEMI identified"
    ],
    "adult---stroke-cva": [
        "No AMS or neurologic deficits",
        "No weakness or facial droop",
        "No slurred speech or aphasia",
        "No seizures or dizziness",
        "No trauma history",
        "No abnormal RACE score",
        "No symptoms onset within 24 hours",
        "No known history of stroke or TIA"
    ],
    "adult---tachycardia-stable": [
        "No chest pain, dizziness, or SOB",
        "No history of palpitations",
        "No ECG abnormalities",
        "No signs of CHF",
        "No hypotension or AMS",
        "No need for adenosine or amiodarone",
        "No irregular or wide complex rhythm"
    ],
    "adult---tachycardia-unstable": [
        "No altered mental status",
        "No hypotension or shock",
        "No signs of unstable rhythm",
        "No need for cardioversion",
        "No wide or polymorphic complex noted",
        "No need for sedation",
        "No medication administered for rate control"
    ],
    "adult---ventilation-management": [
        "No respiratory distress",
        "No need for BVM, CPAP, or intubation",
        "No abnormal breath sounds",
        "No hypoxia or hypercapnia",
        "No airway obstruction noted",
        "No altered mental status impacting ventilation"
    ],
    "pediatric---general-pediatric-assessment": [
        "No abnormal vital signs",
        "No respiratory distress",
        "No mental status changes",
        "No signs of trauma or shock",
        "No chief complaint requiring immediate intervention"
    ],
    "pediatric---general-pediatric-trauma-assessment": [
        "No traumatic mechanism identified",
        "No signs of multisystem trauma",
        "No hypotension or shock",
        "No airway compromise",
        "No neurological deficits"
    ],
    "pediatric---abdominal-flank-pain-nausea-vomiting": [
        "No nausea or vomiting",
        "No abdominal tenderness or pain",
        "No diarrhea or constipation",
        "No urinary complaints",
        "No fever or signs of infection",
        "No need for antiemetic"
    ],
    "pediatric---allergic-reaction": [
        "No itching or hives",
        "No respiratory distress",
        "No throat/chest constriction",
        "No difficulty swallowing",
        "No hypotension or shock",
        "No history of allergen exposure"
    ],
    "pediatric---altered-mental-status": [
        "No decrease in mentation",
        "No blood glucose abnormalities",
        "No trauma or ingestion suspected",
        "No respiratory depression",
        "No seizure or postictal state observed"
    ],
    "pediatric---behavioral-emergencies": [
        "No violent or bizarre behavior",
        "No suicidal or homicidal ideation",
        "No hallucinations or delusions",
        "No injuries or self-harm",
        "No recent trauma or ingestion suspected",
        "No need for physical restraint",
        "No sedation administered",
        "No involvement of law enforcement",
        "No danger to self or others"
    ],
    "pediatric---bradycardia": [
        "No hypotension or signs of shock",
        "No altered mental status",
        "No HR <60 bpm",
        "No respiratory distress",
        "No seizure or syncope",
        "No signs of CHF",
        "No evidence of overdose",
        "No transcutaneous pacing used"
    ],
    "pediatric---burns": [
        "No thermal, chemical, or electrical burns",
        "No facial burns or inhalational injury",
        "No signs of shock or hypotension",
        "No airway compromise",
        "No >10% BSA second-degree burns",
        "No circumferential burns",
        "No CO exposure suspected",
        "No pain or swelling noted",
        "No early intubation needed"
    ],
    "pediatric---cardiac-arrest-non-traumatic": [
        "No unresponsiveness",
        "No apnea or pulselessness",
        "No DNR or prehospital death criteria met",
        "No shockable rhythm detected",
        "No ROSC achieved",
        "No H's and T's identified",
        "No defibrillation needed",
        "No airway management required"
    ],
    "pediatric---cold-related-illness": [
        "No exposure to cold or wet environment",
        "No AMS or coma",
        "No hypothermia (temp normal)",
        "No extremity pain or shivering",
        "No hypotension or bradycardia",
        "No signs of sepsis or trauma",
        "No active warming required"
    ],
    "pediatric---epistaxis": [
        "No nasal bleeding noted",
        "No signs of trauma or foreign body",
        "No anticoagulant or NSAID use",
        "No signs of posterior bleeding",
        "No history of recurrent epistaxis",
        "No difficulty tolerating nasal spray",
        "No history of bleeding disorder",
        "No pain, nausea, or vomiting"
    ],
    "pediatric---heat-related-illness": [
        "No exposure to high temperatures",
        "No altered mental status",
        "No signs of heat stroke (temp >104°F)",
        "No hypotension or seizures",
        "No dehydration or muscle cramps",
        "No need for active cooling or IV fluids"
    ],
    "pediatric---neonatal-resuscitation": [
        "No poor tone or absent cry",
        "No need for BVM or CPR",
        "No HR <100 or <60 bpm",
        "No cyanosis or apnea",
        "No need for epinephrine",
        "No abnormal APGAR scores",
        "No meconium or delivery complications"
    ],
    "pediatric---overdose-poisoning": [
        "No ingestion suspected",
        "No abnormal mental status",
        "No abnormal vital signs",
        "No SLUDGE symptoms or seizures",
        "No antidotes required",
        "No respiratory depression",
        "No signs of toxidrome"
    ],
    "pediatric---pain-management": [
        "No pain reported",
        "No pain score documented",
        "No analgesia required",
        "No trauma or burn noted",
        "No vomiting or nausea post-medication",
        "No respiratory compromise",
        "No allergy to medications"
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
