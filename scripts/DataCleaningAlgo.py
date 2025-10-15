import pandas as pd

# Load your CSV
df = pd.read_csv("synbiohub_parts_export.csv")

# Step 1: Fill blanks to avoid errors
df['type'] = df['type'].fillna('')

# Step 2: Split into two columns, handle missing comma
# Only split on the first comma, so if no comma, SO_term will be NaN
df[['type_clean', 'SO_term']] = df['type'].str.split(',', n=1, expand=True)

# Step 3: Clean whitespace
df['type_clean'] = df['type_clean'].str.strip()
df['SO_term'] = df['SO_term'].str.strip()

# Step 4: Replace empty strings with None
df = df.replace(r'^\s*$', None, regex=True)

# Optional: Drop original 'type' column and rename
df.drop(columns=['type'], inplace=True)
df.rename(columns={'type_clean': 'type'}, inplace=True)

# Save cleaned version
df.to_csv("cleaned_synbiohub_parts.csv", index=False)
