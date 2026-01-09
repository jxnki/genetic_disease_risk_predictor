import math

# --- Carrier frequency by population ---
POPULATION_CARRIER_RATE = {
    "south_asian": 0.08,
    "african": 0.05,
    "european": 0.02
}

# --- Graph‑based relatedness ---
RELATEDNESS = {
    "unrelated": 0.0,
    "second_cousins": 0.03,
    "first_cousins": 0.125
}

# --- Family history evidence ---
HISTORY_SCORE = {
    "none": 0,
    "one_parent": 1,
    "both_parents": 2
}

# Thalassemia is NOT gender‑linked
GENDER_FACTOR = {
    "boy": 1.0,
    "girl": 1.0
}

# --- Weights (importance of each factor) ---
W_POP = 2.5
W_HISTORY = 1.8
W_RELATION = 3.0


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def calculate_thalassemia_risk(
        mother_population,
        father_population,
        relation,
        history,
        gender
    ):

    # 1️⃣ Carrier probabilities
    P_mother = POPULATION_CARRIER_RATE[mother_population]
    P_father = POPULATION_CARRIER_RATE[father_population]

    # 2️⃣ Log carrier score (log(a×b) = log(a)+log(b))
    carrier_score = math.log(P_mother) + math.log(P_father)

    # 3️⃣ Family history score
    history_score = HISTORY_SCORE[history]

    # 4️⃣ Relatedness score
    relation_score = RELATEDNESS[relation] * 10   # scaled

    # 5️⃣ Combined risk score (linear model)
    S = (
        W_POP * carrier_score +
        W_HISTORY * history_score +
        W_RELATION * relation_score
    )

    # 6️⃣ Logistic conversion to probability
    prob = sigmoid(S)

    # 7️⃣ Gender adjustment (neutral for Thalassemia)
    prob = prob * GENDER_FACTOR[gender]

    return prob

if __name__ == "__main__":
    r = calculate_thalassemia_risk(
        mother_population="south_asian",
        father_population="south_asian",
        relation="second_cousins",
        history="both_parents",
        gender="boy"
    )

    print("Thalassemia risk:", round(r * 100, 3), "%")
