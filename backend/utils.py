import re

def extract_details(text):
    text = text.lower()

    # Default values
    income = 200000
    occupation = "Any"
    category = "Health"

    # Extract income
    match = re.search(r'\d+', text)
    if match:
        income = int(match.group())

    # Detect occupation
    if "student" in text:
        occupation = "Student"
        category = "Education"
    elif "farmer" in text:
        occupation = "Farmer"
        category = "Agriculture"
    elif "job" in text or "unemployed" in text:
        occupation = "Unemployed"
        category = "Employment"
    elif "business" in text:
        occupation = "Entrepreneur"
        category = "Business"

    return income, occupation, category