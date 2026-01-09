from flask import Flask, request, jsonify, render_template
from model import calculate_thalassemia_risk
from model_hemophilia import calculate_hemophilia_risk

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/calculate_thalassemia", methods=["POST"])
def calc_thal():
    d = request.json
    # Your model needs a gender input, but returns same risk for both.
    # We call it twice or just once since it's autosomal.
    risk = calculate_thalassemia_risk(
        d['mother_population'], 
        d['father_population'], 
        d['relation'], 
        d['history'], 
        "boy" # Dummy value since gender doesn't change autosomal risk
    )
    return jsonify({ "risk": round(risk * 100, 2) })

@app.route("/calculate_hemophilia", methods=["POST"])
def calc_hemo():
    d = request.json
    res = calculate_hemophilia_risk(
        d['mother_carrier'], 
        d['mother_history'], 
        d['mother_population'], 
        d['father_affected']
    )
    return jsonify({
        "boy": round(res["boy_affected"] * 100, 2),
        "girl_carrier": round(res["girl_carrier"] * 100, 2),
        "girl_affected": round(res["girl_affected"] * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)