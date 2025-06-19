import csv
import os
import requests
import time
from datetime import datetime

overpass_url: str = "http://overpass-api.de/api/interpreter"
max_retries: int = 3

def get_query(area_condition: str, has_species: bool) -> str:
    species_condition = "species" if has_species else "!species"
    return f"""
    [out:json];
    area{area_condition} -> .a;
    node[natural=tree][{species_condition}](area.a);
    out count;
    """

def run_overpass_query(query: str) -> dict:
    for attempt in range(max_retries):
        try:
            response = requests.get(overpass_url, params={'data': query})
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(60)  # Wait for a minute before retrying
                continue
            print("Max retries reached. Could not complete the request.")
            return 0
    return 0

def get_total(area: str, has_species: bool) -> int:
    query = get_query(area, has_species)
    result = run_overpass_query(query)
    if result:
        return int(result['elements'][0]['tags']['total'])
    else:
        return 0

print("Starting retrieval of tree data...")
france_species = get_total('[name="France"]', True)
print(f"Trees in France with species: {france_species}")
france_no_species = get_total('[name="France"]', False)
print(f"Trees in France without species: {france_no_species}")

aura_species = get_total('[name="Auvergne-Rhône-Alpes"]', True)
print(f"Trees in Auvergne-Rhône-Alpes with species: {aura_species}")
aura_no_species = get_total('[name="Auvergne-Rhône-Alpes"]', False)
print(f"Trees in Auvergne-Rhône-Alpes without species: {aura_no_species}")

isere_species = get_total('[name="Isère"]', True)
print(f"Trees in Isère with species: {isere_species}")
isere_no_species = get_total('[name="Isère"]', False)
print(f"Trees in Isère without species: {isere_no_species}")

metro_species = get_total('[name="Grenoble-Alpes Métropole"]', True)
print(f"Trees in Grenoble-Alpes Métropole with species: {metro_species}")
metro_no_species = get_total('[name="Grenoble-Alpes Métropole"]', False)
print(f"Trees in Grenoble-Alpes Métropole without species: {metro_no_species}")

grenoble_species = get_total('[name="Grenoble"][admin_level=8]', True)
print(f"Trees in Grenoble with species: {grenoble_species}")
grenoble_no_species = get_total('[name="Grenoble"][admin_level=8]', False)
print(f"Trees in Grenoble without species: {grenoble_no_species}")

secteur1_species = get_total('[name="Secteur 1"]["addr:postcode"=38000]', True)
print(f"Trees in Secteur 1 with species: {secteur1_species}")
secteur1_no_species = get_total('[name="Secteur 1"]["addr:postcode"=38000]', False)
print(f"Trees in Secteur 1 without species: {secteur1_no_species}")

secteur2_species = get_total('[name="Secteur 2"]["addr:postcode"=38000]', True)
print(f"Trees in Secteur 2 with species: {secteur2_species}")
secteur2_no_species = get_total('[name="Secteur 2"]["addr:postcode"=38000]', False)
print(f"Trees in Secteur 2 without species: {secteur2_no_species}")

secteur3_species = get_total('[name="Secteur 3"]["addr:postcode"=38100]', True)
print(f"Trees in Secteur 3 with species: {secteur3_species}")
secteur3_no_species = get_total('[name="Secteur 3"]["addr:postcode"=38100]', False)
print(f"Trees in Secteur 3 without species: {secteur3_no_species}")

secteur4_species = get_total('[name="Secteur 4"]["addr:postcode"=38100]', True)
print(f"Trees in Secteur 4 with species: {secteur4_species}")
secteur4_no_species = get_total('[name="Secteur 4"]["addr:postcode"=38100]', False)
print(f"Trees in Secteur 4 without species: {secteur4_no_species}")

secteur5_species = get_total('[name="Secteur 5"]["addr:postcode"=38100]', True)
print(f"Trees in Secteur 5 with species: {secteur5_species}")
secteur5_no_species = get_total('[name="Secteur 5"]["addr:postcode"=38100]', False)
print(f"Trees in Secteur 5 without species: {secteur5_no_species}")

secteur6_species = get_total('[name="Secteur 6"]["addr:postcode"=38100]', True)
print(f"Trees in Secteur 6 with species: {secteur6_species}")
secteur6_no_species = get_total('[name="Secteur 6"]["addr:postcode"=38100]', False)
print(f"Trees in Secteur 6 without species: {secteur6_no_species}")

teisseire_species = get_total('[landuse=residential][name="Teisseire"]', True)
print(f"Trees in Teisseire with species: {teisseire_species}")
teisseire_no_species = get_total('[landuse=residential][name="Teisseire"]', False)
print(f"Trees in Teisseire without species: {teisseire_no_species}")

malherbe_species = get_total('[landuse=residential][name="Malherbe"]', True)
print(f"Trees in Malherbe with species: {malherbe_species}")
malherbe_no_species = get_total('[landuse=residential][name="Malherbe"]', False)
print(f"Trees in Malherbe without species: {malherbe_no_species}")

villeneuve_species = get_total('[landuse=residential][name="Villeneuve"]', True)
print(f"Trees in Villeneuve with species: {villeneuve_species}")
villeneuve_no_species = get_total('[landuse=residential][name="Villeneuve"]', False)
print(f"Trees in Villeneuve without species: {villeneuve_no_species}")

vigny_musset_species = get_total('[landuse=residential][name="Vigny Musset"]', True)
print(f"Trees in Vigny Musset with species: {vigny_musset_species}")
vigny_musset_no_species = get_total('[landuse=residential][name="Vigny Musset"]', False)
print(f"Trees in Vigny Musset without species: {vigny_musset_no_species}")

village_olympique_species = get_total('[landuse=residential][name="Village Olympique"]', True)
print(f"Trees in Village Olympique with species: {village_olympique_species}")
village_olympique_no_species = get_total('[landuse=residential][name="Village Olympique"]', False)
print(f"Trees in Village Olympique without species: {village_olympique_no_species}")

echirolles_species = get_total('[name="Échirolles"]', True)
print(f"Trees in Échirolles with species: {echirolles_species}")
echirolles_no_species = get_total('[name="Échirolles"]', False)
print(f"Trees in Échirolles without species: {echirolles_no_species}")

eybens_species = get_total('[name="Eybens"]', True)
print(f"Trees in Eybens with species: {eybens_species}")
eybens_no_species = get_total('[name="Eybens"]', False)
print(f"Trees in Eybens without species: {eybens_no_species}")

saint_martin_species = get_total("[name=\"Saint-Martin-d'Hères\"]", True)
print(f"Trees in Saint-Martin-d'Hères with species: {saint_martin_species}")
saint_martin_no_species = get_total("[name=\"Saint-Martin-d'Hères\"]", False)
print(f"Trees in Saint-Martin-d'Hères without species: {saint_martin_no_species}")

la_tronche_species = get_total('[name="La Tronche"]', True)
print(f"Trees in La Tronche with species: {la_tronche_species}")
la_tronche_no_species = get_total('[name="La Tronche"]', False)
print(f"Trees in La Tronche without species: {la_tronche_no_species}")

fontaine_species = get_total('[name="Fontaine"]', True)
print(f"Trees in Fontaine with species: {fontaine_species}")
fontaine_no_species = get_total('[name="Fontaine"]', False)
print(f"Trees in Fontaine without species: {fontaine_no_species}")

seyssinet_pariset_species = get_total('[name="Seyssinet-Pariset"]', True)
print(f"Trees in Seyssinet-Pariset with species: {seyssinet_pariset_species}")
seyssinet_pariset_no_species = get_total('[name="Seyssinet-Pariset"]', False)
print(f"Trees in Seyssinet-Pariset without species: {seyssinet_pariset_no_species}")

seyssins_species = get_total('[name="Seyssins"]', True)
print(f"Trees in Seyssins with species: {seyssins_species}")
seyssins_no_species = get_total('[name="Seyssins"]', False)
print(f"Trees in Seyssins without species: {seyssins_no_species}")

# Prepare data for CSV
date = datetime.now().strftime("%Y-%m-%d")
data = {
    "date": date,
    "france_species": france_species,
    "france_no_species": france_no_species,
    "aura_species": aura_species,
    "aura_no_species": aura_no_species,
    "isere_species": isere_species,
    "isere_no_species": isere_no_species,
    "metro_species": metro_species,
    "metro_no_species": metro_no_species,
    "grenoble_species": grenoble_species,
    "grenoble_no_species": grenoble_no_species,
    "secteur1_species": secteur1_species,
    "secteur1_no_species": secteur1_no_species,
    "secteur2_species": secteur2_species,
    "secteur2_no_species": secteur2_no_species,
    "secteur3_species": secteur3_species,
    "secteur3_no_species": secteur3_no_species,
    "secteur4_species": secteur4_species,
    "secteur4_no_species": secteur4_no_species,
    "secteur5_species": secteur5_species,
    "secteur5_no_species": secteur5_no_species,
    "secteur6_species": secteur6_species,
    "secteur6_no_species": secteur6_no_species,
    "teisseire_species": teisseire_species,
    "teisseire_no_species": teisseire_no_species,
    "malherbe_species": malherbe_species,
    "malherbe_no_species": malherbe_no_species,
    "villeneuve_species": villeneuve_species,
    "villeneuve_no_species": villeneuve_no_species,
    "vigny_musset_species": vigny_musset_species,
    "vigny_musset_no_species": vigny_musset_no_species,
    "village_olympique_species": village_olympique_species,
    "village_olympique_no_species": village_olympique_no_species,
    "echirolles_species": echirolles_species,
    "echirolles_no_species": echirolles_no_species,
    "eybens_species": eybens_species,
    "eybens_no_species": eybens_no_species,
    "saint_martin_species": saint_martin_species,
    "saint_martin_no_species": saint_martin_no_species,
    "la_tronche_species": la_tronche_species,
    "la_tronche_no_species": la_tronche_no_species,
    "fontaine_species": fontaine_species,
    "fontaine_no_species": fontaine_no_species,
    "seyssinet_pariset_species": seyssinet_pariset_species,
    "seyssinet_pariset_no_species": seyssinet_pariset_no_species,
    "seyssins_species": seyssins_species,
    "seyssins_no_species": seyssins_no_species
}

# CSV file path
csv_file_path = "trees_data.csv"

# Check if the file exists
file_exists = os.path.isfile(csv_file_path)

# Write data to CSV with UTF-8 encoding
with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())
    if not file_exists:
        writer.writeheader()  # Write header only if the file does not exist
    writer.writerow(data)

print(f"Data has been written to {csv_file_path}")
