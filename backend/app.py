from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from utils import extract_details

app = Flask(__name__)
CORS(app)

# -----------------------------
# LOAD DATASET
# -----------------------------
df = pd.read_csv("final_100_schemes.csv")

# Remove any empty rows (important)
df = df.dropna()

# -----------------------------
# ENCODING
# -----------------------------
le_occ = LabelEncoder()
le_cat = LabelEncoder()

df['occupation_enc'] = le_occ.fit_transform(df['occupation'])
df['category_enc'] = le_cat.fit_transform(df['category'])

# Features
X = df[['income_limit','occupation_enc','category_enc']]
y = df.index   # use index instead of name

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# -----------------------------
# RECOMMEND API (TOP 5)
# -----------------------------
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json

    income = data.get('income')
    occupation = data.get('occupation')
    category = data.get('category')

    try:
        occ = le_occ.transform([occupation])[0]
        cat = le_cat.transform([category])[0]
    except:
        return jsonify({"error": "Invalid occupation or category"}), 400

    probs = model.predict_proba([[income, occ, cat]])[0]
    top_indices = probs.argsort()[-5:][::-1]

    results = []

    for idx in top_indices:
        scheme = df.iloc[idx]

        reason = f"Eligible because your income ≤ ₹{scheme['income_limit']} and matches {scheme['occupation']}"

        results.append({
            "name": scheme['scheme_name'],
            "category": scheme['category'],
            "benefit": f"{scheme['benefit_type']} (₹{scheme['benefit_amount']})",
            "description": scheme['description'],
            "reason": reason
        })

    return jsonify({"schemes": results})

# -----------------------------
# CHATBOT API
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get('message')

    income, occupation, category = extract_details(message)

    try:
        occ = le_occ.transform([occupation])[0]
        cat = le_cat.transform([category])[0]
    except:
        return jsonify({"reply": "Sorry, I couldn't understand your profile."})

    pred_index = model.predict([[income, occ, cat]])[0]
    scheme = df.iloc[pred_index]

    reply = f"""
Scheme: {scheme['scheme_name']}
Category: {scheme['category']}
Benefit: ₹{scheme['benefit_amount']} ({scheme['benefit_type']})
Reason: Based on your income and occupation
"""

    return jsonify({"reply": reply})

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)