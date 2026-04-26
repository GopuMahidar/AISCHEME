import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

df = pd.read_excel("large_schemes_dataset.xlsx")

le_occ = LabelEncoder()
le_cat = LabelEncoder()

df['occupation'] = le_occ.fit_transform(df['occupation'])
df['category'] = le_cat.fit_transform(df['category'])

X = df[['income_limit','occupation','category']]
y = df['scheme_name']

model = RandomForestClassifier()
model.fit(X, y)

def predict_scheme(income, occupation, category):
    occ = le_occ.transform([occupation])[0]
    cat = le_cat.transform([category])[0]
    return model.predict([[income, occ, cat]])[0]