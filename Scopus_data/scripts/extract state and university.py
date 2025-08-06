import pandas as pd
import re

# Load the data
df = pd.read_excel(r"/Scopus_data/data/raw/Semi_publication us university_7.14.xlsx")  # your actual path

# US state abbreviations (same as before)
us_states = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC"
}

# Extract state abbreviation
def extract_state(text):
    if pd.isna(text):
        return "Unknown"
    tokens = re.findall(r'\b[A-Z]{2}\b', text)
    for token in reversed(tokens):
        if token in us_states:
            return token
    return "Unknown"

# Extract university name using pattern match
def extract_university_name(text):
    if pd.isna(text):
        return ""
    text = text.strip()

    # Common patterns
    patterns = [
        r"([A-Z][a-z]+(?: [A-Z][a-z]+)* University)",                   # e.g. Arizona State University
        r"(University of [A-Z][a-z]+(?: [A-Z][a-z]+)*)",               # e.g. University of Michigan
        r"([A-Z][a-z]+ Institute of Technology)",                      # e.g. California Institute of Technology
        r"([A-Z][a-z]+ College(?: of [A-Z][a-z]+)*)",                  # e.g. Boston College
        r"([A-Z]{2,}(?: [A-Z]{2,})* University)",                      # e.g. MIT University (rare uppercase acronyms)
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return ""

# Apply to your DataFrame
df["State"] = df["Affiliation"].apply(extract_state)
df["University"] = df["Affiliation"].apply(extract_university_name)

# Save or preview
df.to_csv("us_affiliations_with_university_and_state.csv", index=False)
print(df[["Affiliation", "State", "University"]].head())

