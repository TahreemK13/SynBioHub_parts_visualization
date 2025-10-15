from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import csv

sparql = SPARQLWrapper("https://synbiohub.org/sparql")
sparql.setQuery("""
PREFIX sbol: <http://sbols.org/v2#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?displayId ?name ?type ?created
WHERE {
  ?part a sbol:ComponentDefinition .
  OPTIONAL { ?part sbol:displayId ?displayId . }
  OPTIONAL { ?part sbol:name ?name . }
  OPTIONAL { ?part sbol:role ?type . } 
  OPTIONAL { ?part dcterms:created ?created . }
}
ORDER BY DESC(?created)
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

consolidated = defaultdict(lambda: {"name": "", "types": set(), "created": ""})
for r in results["results"]["bindings"]:
    display_id = r.get("displayId", {}).get("value", "")
    name = r.get("name", {}).get("value", "")
    type_url = r.get("type", {}).get("value", "")
    created = r.get("created", {}).get("value", "")
    if "#" in type_url:
        type_label = type_url.split("#")[-1]
    elif "/" in type_url:
        type_label = type_url.split("/")[-1]
    else:
        type_label = type_url
    if "partType/" in type_label:
        type_label = type_label.split("partType/")[-1]
    consolidated[display_id]["name"] = name
    consolidated[display_id]["types"].add(type_label)
    consolidated[display_id]["created"] = created
data_list = []
for display_id, info in consolidated.items():
    labels = []
    so_ids = []
    for t in info["types"]:
        if t.startswith("SO:"):
            so_ids.append(t)
        else:
            labels.append(t)
    type_str = ", ".join(labels + so_ids)
    entry = {
        "displayId": display_id,
        "type": type_str,
        "created": info["created"] if info["created"] else ""
    }
    data_list.append(entry)

with open("synbiohub_parts_export.csv", "w", newline="") as csvfile:
    fieldnames = ["displayId", "type", "created"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in data_list:
        writer.writerow({
            "displayId": entry["displayId"],
            "type": entry["type"],
            "created": entry["created"]
        })
print("Exported all parts to synbiohub_parts_export.csv without the name column.")
