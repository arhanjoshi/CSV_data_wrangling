import pandas as pd
# === Step 1: Load your dataset ===
file_path = r"Scopus_data/data/processed/Unique Affiliation.xlsx" # 🔁 Replace with your actual CSV file path
df = pd.read_excel(file_path)

# === Step 2: Classification function ===
def classify_affiliation(affiliation):
    aff = str(affiliation).lower()

    # University indicators
    university_keywords = [
        'university', 'school of', 'college of', 'université', 'universität', 'università', 'universidad', 'institute','istituto'
    ]

    # Government indicators (excluding "department of" unless university is absent)
    government_keywords = [
        'national laboratory', 'national institute', 'nist', 'naval research', 'air force research', 'army research',
        'brookhaven', 'argonne', 'government', 'ministry', 'bureau', 'nrel', 'doe', 'usgs', 'nasa',
        'center for bio/molecular science and engineering', 'national renewable energy laboratory', 'national'
    ]

    # Industry indicators
    industry_keywords = [
        'inc', 'llc', 'corp', 'co.', 'corporation', 'technologies', 'solutions', 'company', 'bytedance', 'ltd'
    ]

    # === Priority: University > Industry > Government ===
    if any(kw in aff for kw in university_keywords):
        return 'University Entity'
    elif any(kw in aff for kw in industry_keywords):
        return 'Private/Industry Entity'
    elif 'department of' in aff and not any(kw in aff for kw in university_keywords):
        return 'Government Entity'
    elif any(kw in aff for kw in government_keywords):
        return 'Government Entity'
    else:
        return 'Unknown'

# === Step 3: Apply classification ===
df['Affiliation_Type'] = df['Affiliation'].apply(classify_affiliation)

# === Step 4: Save result ===
output_path = "classified_affiliations.csv"
df.to_csv(output_path, index=False)
print(f"✅ Done! Output saved to: {output_path}")