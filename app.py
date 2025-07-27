from flask import Flask, render_template, request
import json

app = Flask(__name__)

def classify_routine(recommendations):
    morning_keywords=["sunscreen","vitamin c","niacinamide"]
    night_keywords=["retinol","clay mask","scrub"]
    general_keywords=["cleanser","toner","moisturizer"]
    
    morning = []
    night=[]
    general=[]

    for rec in recommendations:
        rec_lower=rec.lower()

        if any(word in rec_lower for word in night_keywords):
            night.append(rec)
        elif any(word in rec_lower for word in morning_keywords):
            morning.append(rec)
        elif any(word in rec_lower for word in general_keywords):
            general.append(rec)
        else:
            general.append(rec)

    return morning,night,general

    

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    skin_type = request.form.get("skin_type")
    concern_input = request.form.get("concern", "").strip()
    concern = concern_input.lower()

    if not skin_type:
        return render_template("result.html",
                               skin_type="Not provided",
                               concern="Not provided",
                               recommendations=["⚠️ Please fill in all the fields before submitting."])

    with open("data/skincare_data.json", "r") as file:
        data = json.load(file)

    skin_data = data.get(skin_type, {})

    if concern == "":
        recommendations = skin_data.get("", ["❗ No concern provided."])
        display_concern = "None"

    elif concern in skin_data:
        recommendations = skin_data[concern]
        display_concern = concern_input

    else:
        recommendations = ["❌ Sorry, we are still researching this concern, stay hydrated and use sunscreen! 🥵"]
        display_concern = f"Invalid concern: '{concern_input}'"

    morning ,night, general=classify_routine(recommendations)

    return render_template("result.html",
                           skin_type=skin_type,
                           concern=display_concern,
                           morning_routine=morning,
                           night_routine=night,
                           general_routine=general)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
