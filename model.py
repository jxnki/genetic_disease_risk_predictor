import math

# --- Carrier frequency by population ---
POPULATION_CARRIER_RATE = {
    "south_asian": 0.08,
    "african": 0.05,
    "european": 0.02
}

# --- Graph-based relatedness ---
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

# --- Weights ---
W_POP = 2.5
W_HISTORY = 1.8
W_RELATION = 3.0


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def calculate_thalassemia_risk(
        mother_population,
        father_population,
        relation,
        history
    ):
    # 1️⃣ Carrier probabilities
    P_mother = POPULATION_CARRIER_RATE[mother_population]
    P_father = POPULATION_CARRIER_RATE[father_population]

    # 2️⃣ Log carrier score
    carrier_score = math.log(P_mother) + math.log(P_father)

    # 3️⃣ Family history score
    history_score = HISTORY_SCORE[history]

    # 4️⃣ Relatedness score
    relation_score = RELATEDNESS[relation] * 10

    # 5️⃣ Combined linear risk score
    S = (
        W_POP * carrier_score +
        W_HISTORY * history_score +
        W_RELATION * relation_score
    )

    # 6️⃣ Logistic probability
    base_prob = sigmoid(S)

    # 7️⃣ Output for both genders
    return {
        "boy": base_prob,
        "girl": base_prob
    }

if __name__ == "__main__":
    r = calculate_thalassemia_risk(
        mother_population="south_asian",
        father_population="european",
        relation="first_cousins",
        history="one_parent"
    )

    print("Risk if BOY:", round(r["boy"] * 100, 3), "%")
    print("Risk if GIRL:", round(r["girl"] * 100, 3), "%")
