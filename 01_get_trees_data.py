import csv
import os
import requests
import time
from datetime import datetime

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[38;5;214m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

overpass_url: str = "http://overpass-api.de/api/interpreter"
max_retries: int = 3

def get_query(area_condition: str, has_species: bool) -> str:
    species_condition = "species" if has_species else "!species"
    return f"""
    [out:json][timeout:360];
    area{area_condition} -> .a;
    node[natural=tree][{species_condition}](area.a);
    out count;
    """

def run_overpass_query(query: str) -> dict:
    for attempt in range(max_retries):
        try:
            response = requests.get(overpass_url, params={'data': query})
            response.raise_for_status()
            data = response.json()
            return int(data['elements'][0]['tags']['total'])
        except Exception as e:
            print(f"{RED}❌ Attempt {attempt + 1} failed: {e}{RESET}")
            time.sleep(60)
    print(f"{RED}❌ All attempts failed. Giving up.{RESET}")
    return None

def get_total(area: str, has_species: bool) -> int:
    query = get_query(area, has_species)
    return run_overpass_query(query)

def print_result(label: str, species: int, no_species: int):
    total = species + no_species
    if total == 0:
        print(f"🌳 {label} - No tree data available.")
        return

    percent = (species * 100) / total
    ratio = species / no_species if no_species > 0 else float('inf')

    # Comparison symbol
    if species > no_species:
        symbol = ">"
        trend = "📈 Good trend: more trees with species"
        color = GREEN
    elif species < no_species:
        symbol = "<"
        trend = "📉 Needs attention: more trees without species"
        color = YELLOW
    else:
        symbol = "="
        trend = "⚖️ Balanced: equal trees with and without species"
        color = BLUE

    print(f"{color}🌳 {label} – {percent:.1f}% of trees with species ({ratio:.2f} ratio){RESET}")
    print(f"{color}   {trend} ({species} {symbol} {no_species}){RESET}")

print(f"{BLUE}📊 Starting tree data retrieval...{RESET}")

france_species = get_total('[name="France"]', True)
france_no_species = get_total('[name="France"]', False)
print_result("France", france_species, france_no_species)

aura_species = get_total('[name="Auvergne-Rhône-Alpes"]', True)
aura_no_species = get_total('[name="Auvergne-Rhône-Alpes"]', False)
print_result("Auvergne-Rhône-Alpes", aura_species, aura_no_species)

isere_species = get_total('[name="Isère"]', True)
isere_no_species = get_total('[name="Isère"]', False)
print_result("Isère", isere_species, isere_no_species)

metro_species = get_total('[name="Grenoble-Alpes Métropole"]', True)
metro_no_species = get_total('[name="Grenoble-Alpes Métropole"]', False)
print_result("Grenoble-Alpes Métropole", metro_species, metro_no_species)

grenoble_species = get_total('[name="Grenoble"][admin_level=8]', True)
grenoble_no_species = get_total('[name="Grenoble"][admin_level=8]', False)
print_result("Grenoble", grenoble_species, grenoble_no_species)

secteur1_species = get_total('[name="Secteur 1"]["addr:postcode"=38000]', True)
secteur1_no_species = get_total('[name="Secteur 1"]["addr:postcode"=38000]', False)
print_result("Grenoble Secteur 1", secteur1_species, secteur1_no_species)

secteur2_species = get_total('[name="Secteur 2"]["addr:postcode"=38000]', True)
secteur2_no_species = get_total('[name="Secteur 2"]["addr:postcode"=38000]', False)
print_result("Grenoble Secteur 2" ,secteur2_species, secteur2_no_species)

secteur3_species = get_total('[name="Secteur 3"]["addr:postcode"=38100]', True)
secteur3_no_species = get_total('[name="Secteur 3"]["addr:postcode"=38100]', False)
print_result("Grenoble Secteur 3", secteur3_species, secteur3_no_species)

secteur4_species = get_total('[name="Secteur 4"]["addr:postcode"=38100]', True)
secteur4_no_species = get_total('[name="Secteur 4"]["addr:postcode"=38100]', False)
print_result("Grenoble Secteur 4", secteur4_species, secteur4_no_species)

secteur5_species = get_total('[name="Secteur 5"]["addr:postcode"=38100]', True)
secteur5_no_species = get_total('[name="Secteur 5"]["addr:postcode"=38100]', False)
print_result("Grenoble Secteur 5", secteur5_species, secteur5_no_species)

secteur6_species = get_total('[name="Secteur 6"]["addr:postcode"=38100]', True)
secteur6_no_species = get_total('[name="Secteur 6"]["addr:postcode"=38100]', False)
print_result("Grenoble Secteur 6", secteur6_species, secteur6_no_species)

teisseire_species = get_total('[landuse=residential][name="Teisseire"]', True)
teisseire_no_species = get_total('[landuse=residential][name="Teisseire"]', False)
print_result("Grenoble Teisseire", teisseire_species, teisseire_no_species)

malherbe_species = get_total('[landuse=residential][name="Malherbe"]', True)
malherbe_no_species = get_total('[landuse=residential][name="Malherbe"]', False)
print_result("Grenoble Malherbe", malherbe_species, malherbe_no_species)

villeneuve_species = get_total('[landuse=residential][name="Villeneuve"]', True)
villeneuve_no_species = get_total('[landuse=residential][name="Villeneuve"]', False)
print_result("Grenoble Villeneuve", villeneuve_species, villeneuve_no_species)

vigny_musset_species = get_total('[landuse=residential][name="Vigny Musset"]', True)
vigny_musset_no_species = get_total('[landuse=residential][name="Vigny Musset"]', False)
print_result("Grenoble Vigny Musset", vigny_musset_species, vigny_musset_no_species)

village_olympique_species = get_total('[landuse=residential][name="Village Olympique"]', True)
village_olympique_no_species = get_total('[landuse=residential][name="Village Olympique"]', False)
print_result("Grenoble Village Olympique", village_olympique_species, village_olympique_no_species)

echirolles_species = get_total('[name="Échirolles"][admin_level=8]', True)
echirolles_no_species = get_total('[name="Échirolles"][admin_level=8]', False)
print_result("Échirolles", echirolles_species, echirolles_no_species)

eybens_species = get_total('[name="Eybens"][admin_level=8]', True)
eybens_no_species = get_total('[name="Eybens"][admin_level=8]', False)
print_result("Eybens", eybens_species, eybens_no_species)

saint_martin_species = get_total("[name=\"Saint-Martin-d'Hères\"][admin_level=8]", True)
saint_martin_no_species = get_total("[name=\"Saint-Martin-d'Hères\"][admin_level=8]", False)
print_result("Saint-Martin-d'Hères", saint_martin_species, saint_martin_no_species)

la_tronche_species = get_total('[name="La Tronche"][admin_level=8]', True)
la_tronche_no_species = get_total('[name="La Tronche"][admin_level=8]', False)
print_result("La Tronche", la_tronche_species, la_tronche_no_species)

fontaine_species = get_total('[name="Fontaine"][admin_level=8]', True)
fontaine_no_species = get_total('[name="Fontaine"][admin_level=8]', False)
print_result("Fontaine", fontaine_species, fontaine_no_species)

seyssinet_pariset_species = get_total('[name="Seyssinet-Pariset"][admin_level=8]', True)
seyssinet_pariset_no_species = get_total('[name="Seyssinet-Pariset"][admin_level=8]', False)
print_result("Seyssinet-Pariset", seyssinet_pariset_species, seyssinet_pariset_no_species)

seyssins_species = get_total('[name="Seyssins"]', True)
seyssins_no_species = get_total('[name="Seyssins"]', False)
print_result("Seyssins", seyssins_species, seyssins_no_species)

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

print(f"{BLUE}📁 Data saved to {csv_file_path}{RESET}")
