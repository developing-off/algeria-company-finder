import os
import googlemaps
from dotenv import load_dotenv
import pandas as pd
from typing import List, Dict, Tuple
import time
import re
import unicodedata

# Dictionnaire des wilayas algériennes avec leurs codes et préfixes postaux
ALGERIA_WILAYAS = {
    'Adrar': {'code': '01', 'postal_prefix': '01'},
    'Chlef': {'code': '02', 'postal_prefix': '02'},
    'Laghouat': {'code': '03', 'postal_prefix': '03'},
    'Oum El Bouaghi': {'code': '04', 'postal_prefix': '04'},
    'Batna': {'code': '05', 'postal_prefix': '05'},
    'Béjaïa': {'code': '06', 'postal_prefix': '06'},
    'Biskra': {'code': '07', 'postal_prefix': '07'},
    'Béchar': {'code': '08', 'postal_prefix': '08'},
    'Blida': {'code': '09', 'postal_prefix': '09'},
    'Bouira': {'code': '10', 'postal_prefix': '10'},
    'Tamanrasset': {'code': '11', 'postal_prefix': '11'},
    'Tébessa': {'code': '12', 'postal_prefix': '12'},
    'Tlemcen': {'code': '13', 'postal_prefix': '13'},
    'Tiaret': {'code': '14', 'postal_prefix': '14'},
    'Tizi Ouzou': {'code': '15', 'postal_prefix': '15'},
    'Alger': {'code': '16', 'postal_prefix': '16'},
    'Djelfa': {'code': '17', 'postal_prefix': '17'},
    'Jijel': {'code': '18', 'postal_prefix': '18'},
    'Sétif': {'code': '19', 'postal_prefix': '19'},
    'Saïda': {'code': '20', 'postal_prefix': '20'},
    'Skikda': {'code': '21', 'postal_prefix': '21'},
    'Sidi Bel Abbès': {'code': '22', 'postal_prefix': '22'},
    'Annaba': {'code': '23', 'postal_prefix': '23'},
    'Guelma': {'code': '24', 'postal_prefix': '24'},
    'Constantine': {'code': '25', 'postal_prefix': '25'},
    'Médéa': {'code': '26', 'postal_prefix': '26'},
    'Mostaganem': {'code': '27', 'postal_prefix': '27'},
    'M\'Sila': {'code': '28', 'postal_prefix': '28'},
    'Mascara': {'code': '29', 'postal_prefix': '29'},
    'Ouargla': {'code': '30', 'postal_prefix': '30'},
    'Oran': {'code': '31', 'postal_prefix': '31'},
    'El Bayadh': {'code': '32', 'postal_prefix': '32'},
    'Illizi': {'code': '33', 'postal_prefix': '33'},
    'Bordj Bou Arréridj': {'code': '34', 'postal_prefix': '34'},
    'Boumerdès': {'code': '35', 'postal_prefix': '35'},
    'El Tarf': {'code': '36', 'postal_prefix': '36'},
    'Tindouf': {'code': '37', 'postal_prefix': '37'},
    'Tissemsilt': {'code': '38', 'postal_prefix': '38'},
    'El Oued': {'code': '39', 'postal_prefix': '39'},
    'Khenchela': {'code': '40', 'postal_prefix': '40'},
    'Souk Ahras': {'code': '41', 'postal_prefix': '41'},
    'Tipaza': {'code': '42', 'postal_prefix': '42'},
    'Mila': {'code': '43', 'postal_prefix': '43'},
    'Aïn Defla': {'code': '44', 'postal_prefix': '44'},
    'Naâma': {'code': '45', 'postal_prefix': '45'},
    'Aïn Témouchent': {'code': '46', 'postal_prefix': '46'},
    'Ghardaïa': {'code': '47', 'postal_prefix': '47'},
    'Relizane': {'code': '48', 'postal_prefix': '48'},
    'Timimoun': {'code': '49', 'postal_prefix': '49'},
    'Bordj Badji Mokhtar': {'code': '50', 'postal_prefix': '50'},
    'Ouled Djellal': {'code': '51', 'postal_prefix': '51'},
    'Béni Abbès': {'code': '52', 'postal_prefix': '52'},
    'In Salah': {'code': '53', 'postal_prefix': '53'},
    'In Guezzam': {'code': '54', 'postal_prefix': '54'},
    'Touggourt': {'code': '55', 'postal_prefix': '55'},
    'Djanet': {'code': '56', 'postal_prefix': '56'},
    'El M\'Ghair': {'code': '57', 'postal_prefix': '57'},
    'El Meniaa': {'code': '58', 'postal_prefix': '58'}
}

# Coordonnées des wilayas (centres approximatifs)
WILAYA_COORDINATES = {
    'Adrar': (27.8742, -0.2939), 'Chlef': (36.1691, 1.3338), 'Laghouat': (33.8000, 2.8650),
    'Oum El Bouaghi': (35.8750, 7.1139), 'Batna': (35.5550, 6.1742), 'Béjaïa': (36.7508, 5.0567),
    'Biskra': (34.8500, 5.7280), 'Béchar': (31.6182, -2.2157), 'Blida': (36.4700, 2.8300),
    'Bouira': (36.3800, 3.9000), 'Tamanrasset': (22.7850, 5.5228), 'Tébessa': (35.4000, 8.1200),
    'Tlemcen': (34.8827, -1.3167), 'Tiaret': (35.3700, 1.3200), 'Tizi Ouzou': (36.7169, 4.0474),
    'Alger': (36.7538, 3.0588), 'Djelfa': (34.6700, 3.2500), 'Jijel': (36.8000, 5.7500),
    'Sétif': (36.1900, 5.4100), 'Saïda': (34.8300, 0.1500), 'Skikda': (36.8667, 6.9000),
    'Sidi Bel Abbès': (35.2000, -0.6300), 'Annaba': (36.9000, 7.7500), 'Guelma': (36.4600, 7.4300),
    'Constantine': (36.3650, 6.6147), 'Médéa': (36.2675, 2.7500), 'Mostaganem': (35.9300, 0.0900),
    'M\'Sila': (35.7000, 4.5400), 'Mascara': (35.4000, 0.1400), 'Ouargla': (31.9500, 5.3300),
    'Oran': (35.6969, -0.6331), 'El Bayadh': (33.6800, 1.0200), 'Illizi': (26.5000, 8.4800),
    'Bordj Bou Arréridj': (36.0700, 4.7600), 'Boumerdès': (36.7600, 3.4800), 'El Tarf': (36.7670, 8.3137),
    'Tindouf': (27.6731, -8.1400), 'Tissemsilt': (35.6000, 1.8100), 'El Oued': (33.3680, 6.8516),
    'Khenchela': (35.4300, 7.1400), 'Souk Ahras': (36.2800, 7.9500), 'Tipaza': (36.5892, 2.4483),
    'Mila': (36.4500, 6.2600), 'Aïn Defla': (36.2500, 1.9700), 'Naâma': (33.2667, -0.3167),
    'Aïn Témouchent': (35.3000, -1.1400), 'Ghardaïa': (32.4900, 3.6700), 'Relizane': (35.7373, 0.5558),
    'Timimoun': (29.2639, 0.2306), 'Bordj Badji Mokhtar': (21.6800, 0.9500),
    'Ouled Djellal': (34.4167, 5.0667), 'Béni Abbès': (30.1300, -2.1700),
    'In Salah': (27.1964, 2.4800), 'In Guezzam': (19.5700, 5.7700),
    'Touggourt': (33.1000, 6.0667), 'Djanet': (24.5500, 9.4800),
    'El M\'Ghair': (33.9500, 5.9200), 'El Meniaa': (30.5789, 2.8789)
}

# Noms alternatifs des wilayas (français, arabe, variations communes)
WILAYA_ALTERNATIVES = {
    'Adrar': ['Adrar', 'ادرار'],
    'Timimoun': ['Timimoun', 'تيميمون', 'Timimoune'],
    'Bordj Badji Mokhtar': ['Bordj Badji Mokhtar', 'برج باجي مختار', 'BBM'],
    'Béni Abbès': ['Béni Abbès', 'بني عباس', 'Beni Abbes'],
    'In Salah': ['In Salah', 'عين صالح', 'Ain Salah', 'In Saleh'],
    'In Guezzam': ['In Guezzam', 'عين قزام', 'Ain Guezzam'],
    'Touggourt': ['Touggourt', 'تقرت', 'Tugurt', 'Touggurt'],
    'Djanet': ['Djanet', 'جانت', 'Janet'],
    'El M\'Ghair': ['El M\'Ghair', 'المغير', 'El Meghaier', 'El-Mgheir'],
    'El Meniaa': ['El Meniaa', 'المنيعة', 'El Menia', 'El-Meniaa']
}

def load_api_key() -> str:
    """Charge la clé API Google Maps depuis le fichier .env"""
    load_dotenv()
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        raise ValueError("Veuillez définir GOOGLE_MAPS_API_KEY dans votre fichier .env")
    return api_key

def initialize_gmaps_client() -> googlemaps.Client:
    """Initialise le client Google Maps"""
    api_key = load_api_key()
    return googlemaps.Client(key=api_key)

def get_wilaya_info(address_components: list) -> dict:
    """Extrait les informations de la wilaya depuis les composants d'adresse"""
    wilaya_name = next((comp['long_name'] for comp in address_components 
                       if 'administrative_area_level_1' in comp['types']), '')
    
    wilaya_name = wilaya_name.replace('Wilaya d\'', '').replace('Wilaya de ', '')
    
    for key, info in ALGERIA_WILAYAS.items():
        if key.lower() in wilaya_name.lower():
            return {
                'name': key,
                'code': info['code'],
                'postal_prefix': info['postal_prefix']
            }
    return {'name': wilaya_name, 'code': '', 'postal_prefix': ''}

def extract_postal_code(address_components: list, wilaya_info: dict) -> str:
    """Extrait et valide le code postal depuis les composants d'adresse"""
    postal_code = next((comp['long_name'] for comp in address_components 
                       if 'postal_code' in comp['types']), '')
    
    if not postal_code:
        for comp in address_components:
            match = re.search(r'\b\d{5}\b', comp['long_name'])
            if match:
                postal_code = match.group(0)
                break
    
    if postal_code and len(postal_code) == 5:
        prefix = postal_code[:2]
        if prefix == wilaya_info['postal_prefix']:
            return postal_code
    
    return f"{wilaya_info['postal_prefix']}000"

def normalize_text(text: str) -> str:
    """Normalise le texte en supprimant les accents et en standardisant les espaces"""
    if not text:
        return ''
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = ' '.join(text.split())
    return text.lower().strip()

def is_duplicate_location(new_loc: Dict, existing_locations: List[Dict]) -> bool:
    """
    Check if a location is a duplicate using multiple strict criteria.
    """
    for existing in existing_locations:
        # Check if coordinates are very close (within ~25 meters)
        # Reduced from 0.0005 (~50m) to 0.00025 (~25m) for more precision
        if abs(new_loc['latitude'] - existing['latitude']) < 0.00025 and \
           abs(new_loc['longitude'] - existing['longitude']) < 0.00025:
            return True
        
        # Normalize and compare names
        new_name = normalize_text(new_loc['name'])
        existing_name = normalize_text(existing['name'])
        
        # Check for name similarity (exact match or one contains the other)
        names_match = (new_name == existing_name or 
                      new_name in existing_name or 
                      existing_name in new_name)
        
        # Compare addresses and vicinity
        new_vicinity = normalize_text(new_loc['vicinity'] or '')
        existing_vicinity = normalize_text(existing['vicinity'] or '')
        new_address = normalize_text(new_loc['address'] or '')
        existing_address = normalize_text(existing['address'] or '')
        
        # Check if addresses or vicinity match
        address_match = (
            (new_vicinity and existing_vicinity and 
             (new_vicinity == existing_vicinity or 
              new_vicinity in existing_vicinity or 
              existing_vicinity in new_vicinity)) or
            (new_address and existing_address and 
             (new_address == existing_address or
              new_address in existing_address or
              existing_address in new_address))
        )
        
        # Check if phone numbers match (when available)
        phone_match = (new_loc.get('phone') and existing.get('phone') and 
                      normalize_text(new_loc['phone']) == normalize_text(existing['phone']))
        
        # Additional validation: check postal codes and communes
        postal_match = (new_loc.get('postal_code') == existing.get('postal_code'))
        commune_match = (normalize_text(new_loc.get('commune', '')) == 
                        normalize_text(existing.get('commune', '')))
        
        # Consider it a duplicate if:
        # 1. Names match AND (addresses match OR postal codes match OR communes match)
        # 2. Phone numbers match (if available)
        # 3. Very close coordinates AND (names match OR addresses match)
        if (names_match and (address_match or postal_match or commune_match)) or \
           phone_match or \
           (abs(new_loc['latitude'] - existing['latitude']) < 0.00025 and 
            abs(new_loc['longitude'] - existing['longitude']) < 0.00025 and 
            (names_match or address_match)):
            return True
    
    return False

def clean_phone_number(phone: str) -> str:
    """Standardize phone number format."""
    if not phone:
        return ''
    # Remove all non-digit characters except '+'
    cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
    # Ensure proper Algeria country code format
    if cleaned.startswith('00213'):
        cleaned = '+213' + cleaned[5:]
    elif cleaned.startswith('0') and len(cleaned) == 10:
        cleaned = '+213' + cleaned[1:]
    return cleaned

def clean_arabic_text(text: str) -> str:
    """Clean and normalize Arabic text."""
    if not text:
        return ''
    # Remove any HTML entities
    text = text.replace('&nbsp;', ' ')
    # Normalize Arabic characters
    text = unicodedata.normalize('NFKC', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def is_valid_company_name(found_name: str, search_name: str) -> bool:
    """Vérifie si le nom trouvé correspond à l'entreprise recherchée"""
    found_normalized = normalize_text(found_name)
    search_normalized = normalize_text(search_name)
    
    if found_normalized == search_normalized:
        return True
    
    found_words = found_normalized.split()
    search_words = search_normalized.split()
    
    try:
        last_index = -1
        for search_word in search_words:
            found_index = -1
            for i, found_word in enumerate(found_words):
                if i > last_index and search_word == found_word:
                    found_index = i
                    break
            if found_index == -1:
                return False
            last_index = found_index
        return True
    except:
        return False

def generate_search_queries(company_name: str, wilaya_name: str) -> List[str]:
    """Génère plusieurs requêtes de recherche pour une meilleure couverture"""
    queries = []
    
    clean_company = company_name.strip()
    clean_wilaya = wilaya_name.strip()
    
    base_query = f'"{clean_company}" {clean_wilaya}'
    queries.append(f"{base_query} Algeria")
    queries.append(f"{base_query} Algérie")
    queries.append(f'"{clean_company}" agence {clean_wilaya}')
    queries.append(f'"{clean_company}" livraison {clean_wilaya}')
    
    if wilaya_name in WILAYA_ALTERNATIVES:
        for alt_name in WILAYA_ALTERNATIVES[wilaya_name]:
            queries.append(f'"{clean_company}" {alt_name}')
            queries.append(f'"{clean_company}" agence {alt_name}')
    
    return list(set(queries))

def search_in_wilaya(client: googlemaps.Client, company_name: str, wilaya_name: str, 
                    coordinates: Tuple[float, float], language: str) -> List[Dict]:
    """Recherche les emplacements d'une entreprise dans une wilaya spécifique"""
    locations = []
    queries = generate_search_queries(company_name, wilaya_name)
    
    for query in queries:
        try:
            for lang in ['fr', 'en', 'ar'] if language == 'both' else [language]:
                search_result = client.places(
                    query,
                    location=coordinates,
                    radius=50000,
                    language=lang,
                    type='establishment'
                )

                if not search_result.get('results'):
                    search_result = client.places_nearby(
                        location=coordinates,
                        radius=50000,
                        keyword=f'"{company_name}"',
                        language=lang
                    )

                for place in search_result.get('results', []):
                    if not is_valid_company_name(place['name'], company_name):
                        continue
                    
                    details = client.place(place['place_id'], fields=[
                        'formatted_address',
                        'geometry',
                        'name',
                        'address_component',
                        'vicinity',
                        'international_phone_number',
                        'website',
                        'opening_hours'
                    ], language=lang)['result']
                    
                    if not is_valid_company_name(details['name'], company_name):
                        continue
                    
                    location_data = process_place_details(details, wilaya_name, lang)
                    
                    if location_data and not is_duplicate_location(location_data, locations):
                        locations.append(location_data)
                
                time.sleep(2)
                
        except Exception as e:
            print(f"Erreur lors de la recherche '{query}' dans {wilaya_name}: {str(e)}")
            continue
    
    return locations

def process_place_details(details: Dict, wilaya_name: str, lang: str) -> Dict:
    """Traite et valide les détails d'un emplacement"""
    try:
        address_components = details.get('address_components', [])
        wilaya_info = get_wilaya_info(address_components)
        
        if not wilaya_info['code'] or wilaya_name.lower() not in wilaya_info['name'].lower():
            return None
            
        commune = next((comp['long_name'] for comp in address_components 
                       if 'locality' in comp['types']), '')
        postal_code = extract_postal_code(address_components, wilaya_info)
        
        return {
            'name': clean_arabic_text(details.get('name', '')),
            'address': clean_arabic_text(details.get('formatted_address', '')),
            'vicinity': clean_arabic_text(details.get('vicinity', '')),
            'wilaya_name': wilaya_info['name'],
            'wilaya_code': wilaya_info['code'],
            'commune': clean_arabic_text(commune),
            'postal_code': postal_code,
            'phone': clean_phone_number(details.get('international_phone_number', '')),
            'website': details.get('website', ''),
            'latitude': details['geometry']['location']['lat'],
            'longitude': details['geometry']['location']['lng'],
            'language': lang
        }
    except Exception as e:
        print(f"Erreur lors du traitement des détails: {str(e)}")
        return None

def search_company_locations(client: googlemaps.Client, company_name: str, language: str = 'en') -> List[Dict]:
    """Recherche tous les emplacements d'une entreprise dans toutes les wilayas d'Algérie"""
    all_locations = []
    
    for wilaya_name, coordinates in WILAYA_COORDINATES.items():
        print(f"\nRecherche dans {wilaya_name} (Code: {ALGERIA_WILAYAS[wilaya_name]['code']})...")
        locations = search_in_wilaya(client, company_name, wilaya_name, coordinates, language)
        all_locations.extend(locations)
        
        if locations:
            print(f"Trouvé {len(locations)} emplacement(s) dans {wilaya_name}")
        
    return all_locations

def save_to_csv(locations: List[Dict], company_name: str):
    """Enregistre les résultats dans un fichier CSV"""
    if not locations:
        print("Aucun emplacement trouvé.")
        return
    
    locations.sort(key=lambda x: (x['wilaya_code'], x['name']))
    df = pd.DataFrame(locations)
    filename = f"{company_name.replace(' ', '_').lower()}_locations.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\nRésultats enregistrés dans {filename}")

def main():
    try:
        company_name = input("Entrez le nom de l'entreprise à rechercher: ").strip()
        
        while True:
            lang_choice = input("Choisissez la langue (en/fr/both): ").strip().lower()
            if lang_choice in ['en', 'fr', 'both']:
                break
            print("Choix invalide. Veuillez entrer 'en', 'fr', ou 'both'.")
        
        client = initialize_gmaps_client()
        
        print(f"\nRecherche des emplacements de {company_name} dans toutes les wilayas d'Algérie...")
        print("Cela peut prendre plusieurs minutes...")
        
        locations = search_company_locations(client, company_name, lang_choice)
        
        if locations:
            print(f"\nTrouvé {len(locations)} emplacement(s) unique(s):")
            for i, loc in enumerate(locations, 1):
                print(f"\nEmplacement {i}:")
                print(f"Nom: {loc['name']}")
                print(f"Adresse: {loc['address']}")
                print(f"Voisinage: {loc['vicinity']}")
                print(f"Wilaya: {loc['wilaya_name']} (Code: {loc['wilaya_code']})")
                print(f"Commune: {loc['commune']}")
                print(f"Code Postal: {loc['postal_code']}")
                if loc['phone']:
                    print(f"Téléphone: {loc['phone']}")
                print(f"Coordonnées: {loc['latitude']}, {loc['longitude']}")
                print(f"Langue: {loc['language']}")
            
            save_to_csv(locations, company_name)
        else:
            print(f"\nAucun emplacement trouvé pour {company_name} en Algérie.")
            
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")

if __name__ == "__main__":
    main() 