from flask import Flask, request, jsonify, render_template
from model import calculate_thalassemia_risk
from model_hemophilia import calculate_hemophilia_risk
from plots import create_thalassemia_plot, create_hemophilia_plot

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
    # Prepare response fields required by the frontend
    boy_pct = round(risk * 100, 2)
    girl_pct = boy_pct
    girl_carrier_pct = 0.0
    girl_affected_pct = 0.0
    plot_b64 = create_thalassemia_plot(risk)

    return jsonify({
        "boy": boy_pct,
        "girl": girl_pct,
        "girl_carrier": girl_carrier_pct,
        "girl_affected": girl_affected_pct,
        "plot": plot_b64
    })

@app.route("/calculate_hemophilia", methods=["POST"])
def calc_hemo():
    d = request.json
    res = calculate_hemophilia_risk(
        d['mother_carrier'], 
        d['mother_history'], 
        d['mother_population'], 
        d['father_affected']
    )
    boy_pct = round(res["boy_affected"] * 100, 2)
    girl_carrier_pct = round(res["girl_carrier"] * 100, 2)
    girl_affected_pct = round(res["girl_affected"] * 100, 2)
    # 'girl' represents the chance a girl is either carrier or affected
    girl_pct = round((res["girl_carrier"] + res["girl_affected"]) * 100, 2)

    plot_b64 = create_hemophilia_plot(
        res["boy_affected"], res["girl_carrier"], res["girl_affected"]
    )

    return jsonify({
        "boy": boy_pct,
        "girl": girl_pct,
        "girl_carrier": girl_carrier_pct,
        "girl_affected": girl_affected_pct,
        "plot": plot_b64
    })

if __name__ == "__main__":
    app.run(debug=True)