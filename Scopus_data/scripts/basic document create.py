import pandas as pd
import glob
import os

# Load the spreadsheet
csv_dir = "../data/raw/"
file_path = glob.glob(os.path.join(csv_dir, 'combined_semiconductor_publications.csv'))
df = pd.read_csv(file_path)

records = []
mismatched_rows = []

for _, row in df.iterrows():
    year = row['Year']
    doi = row['DOI']
    authors_raw = str(row['Authors'])
    author_ids_raw = str(row['Author(s) ID'])
    affil_raw = str(row['Authors with affiliations'])

    # Step 1: Extract authors and IDs (same order)
    authors = [a.strip() for a in authors_raw.split(';') if a.strip()]
    author_ids = [a.strip() for a in author_ids_raw.split(';') if a.strip()]

    # Safety check
    if len(authors) != len(author_ids):
        print(f"⚠️ Mismatch in number of authors and IDs at DOI {doi}. Skipping.")
        mismatched_rows.append(row)
        continue

    # ✅ This and everything below should be INSIDE the for-loop
    author_id_pairs = list(zip(authors, author_ids))

    # Step 2: Extract affiliations
    affil_entries = [entry.strip() for entry in affil_raw.split(';') if entry.strip()]
    affil_map = {}
    for entry in affil_entries:
        parts = entry.split(',', 1)
        if len(parts) == 2:
            name = parts[0].strip()
            affiliation = parts[1].strip()
            affil_map[name] = affiliation

    # Step 3: Combine info per author
    for name, aid in author_id_pairs:
        matched_affil = ''
        for affil_name in affil_map:
            if name.startswith(affil_name):
                matched_affil = affil_map[affil_name]
                break

        records.append({
            'Year': year,
            'DOI': doi,
            'Author': name,
            'Author_ID': aid,
            'Affiliation': matched_affil
        })

# Save the matched author-paper rows
output_df = pd.DataFrame(records)
output_df.to_csv("final_author_database.csv", index=False)

# Save the mismatched rows separately
if mismatched_rows:
    mismatched_df = pd.DataFrame(mismatched_rows)
    mismatched_df.to_csv("mismatched_rows.csv", index=False)
    print(f"⚠️ Saved {len(mismatched_rows)} mismatched rows to mismatched_rows.csv")

print(f"✅ Done. Output saved with {len(output_df)} author-level entries.")

