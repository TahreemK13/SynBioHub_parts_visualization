# 📈 Growth of SynBioHub Parts by Type (2002–2016)

<img width="1118" height="619" alt="Screenshot 2025-10-14 at 10 45 28 PM" src="https://github.com/user-attachments/assets/8ff25cb3-b0e7-40de-bad3-211f98468aad" />




## Live Visualization

An interactive **Altair** visualization showing how the counts of synthetic biology parts in [SynBioHub](https://synbiohub.org/) has fluctuated over time. The data points are distinguished by the biological type attached to their repository submission (e.g., *Plasmid*, *Composite*, *Promoter*, etc.). View the interactive chart here:  
👉 [SynBioHub Parts Visualization](https://tahreemk13.github.io/SynBioHub_parts_visualization/)
---

## Overview

This visualization explores trends in "part" submissions to SynBioHub from 2002–2016, using the repository’s RDF metadata.  
Each line represents a distinct biological type, with interactive highlighting via the legend.

- **Hover over data points:** view yearly part counts  
- **Click legend:** focus on individual part types  
- **Drag / zoom:** explore the lines of the graph closer, especially where many of them are grouped together

---

## Output

Open the interactive chart directly in your browser:

---

## Data

- **Source:** [SynBioHub](https://synbiohub.org/) public repository
- **Query type:** SPARQL (via the SynBioHub query interface)
- **Fields extracted:**
  - `created` — ISO8601 timestamp of part creation
  - `type` — biological part type tag or ontology label
- **Note:** `created` *reflects the original registration date, not the last update.*  
  For recent changes, the `sbh:modified` field will be used in the next update.

### Example SPARQL query
```sparql
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX sbh: <http://wiki.synbiohub.org/wiki/Terms/synbiohub#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?part ?typeLabel ?created
WHERE {
  ?part rdf:type ?type .
  OPTIONAL { ?type rdfs:label ?typeLabel . }
  ?part dcterms:created ?created .
}

---          
                            **Data Cleaning**

The raw CSV is generated partially cleaned from the initial query from the site. The CSV is then cleaned with pandas to make it uniform:

Parse created timestamps → extract year

Replace missing type entries with "Unidentified"

Drop ontology identifiers (SO:#######)

Aggregate counts by year × type

Output saved to:

data/cleaned_synbiohub_parts.csv

---
                         **Running the Visualization**
1. Setup environment

python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

2. Run the chart script
python scripts/altairsb.py


Output will be created in:

outputs/chart.html
and 
https://tahreemk13.github.io/SynBioHub_parts_visualization/

📂 Project Structure
synbiohub-parts-trend/
├── data/
│   └── cleaned_synbiohub_parts.csv
├── outputs/
│   └── chart.html
├── scripts/
│   ├── altairsb.py
│   ├── DataCleaningAlgo.py
│   └── synbiohub_parts.py
├── README.md
├── requirements.txt
└── venv/        # (ignored in Git)

---  
                        ** Technologies Used **

Python 3.12

pandas — data cleaning and transformation

Altair / Vega-Lite — interactive visualization

SPARQL — for querying RDF-based SynBioHub data

---
                    ** Interpretation and Context **

The rapid growth in Plasmid and Composite part types after 2007 coincides with the expansion of the iGEM registry.

Slower growth after ~2016 reflects dataset limits (created timestamp only), not necessarily reduced submissions.

---
                            **Future Work**

Incorporate sbh:modified to include recent activity

Add facet or filter controls (by registry or collection)

Automate data retrieval via Python SPARQLWrapper

---
                              **Licenses**

Code: MIT License

Data: SynBioHub data remains under original open access terms

Author:
Tahreem Karim
Data Science & Synthetic Biology
