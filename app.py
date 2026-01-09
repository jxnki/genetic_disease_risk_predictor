from flask import Flask, request, jsonify
from model import calculate_thalassemia_risk

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    mother_population = data["mother_population"]
    father_population = data["father_population"]
    relation = data["relation"]
    history = data["history"]

    result = calculate_thalassemia_risk(
        mother_population,
        father_population,
        relation,
        history
    )

    # Convert to percentages
    boy = round(result["boy"] * 100, 3)
    girl = round(result["girl"] * 100, 3)

    # Risk level
    avg = (boy + girl) / 2
    if avg < 5:
        level = "Low"
    elif avg < 15:
        level = "Medium"
    else:
        level = "High"

    return jsonify({
        "boy": boy,
        "girl": girl,
        "risk_level": level
    })

@app.route("/", methods=["GET"])
def index():
    return "API running — use POST /calculate"

if __name__ == "__main__":
    app.run(debug=True)
