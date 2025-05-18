import os
import googlemaps
from dotenv import load_dotenv
import pandas as pd
from typing import List, Dict, Tuple
import time
import re
import unicodedata

# Dictionary of Algerian wilayas with their codes and postal code prefixes
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

# Wilaya coordinates (approximate centers)
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

# Alternative names and search patterns for wilayas
WILAYA_ALTERNATIVES = {
    'Adrar': ['Adrar', 'ادرار'],
    'Timimoun': ['Timimoun', 'تيميمون', 'Timimoune', 'Timimoun Adrar', 'تيميمون ادرار'],
    'Bordj Badji Mokhtar': ['Bordj Badji Mokhtar', 'برج باجي مختار', 'BBM', 'Bordj Badji', 'Bordj Mokhtar'],
    'Béni Abbès': ['Béni Abbès', 'بني عباس', 'Beni Abbes', 'Beni-Abbes', 'Béni-Abbès'],
    'In Salah': ['In Salah', 'عين صالح', 'Ain Salah', 'In Saleh', 'Ain-Salah', 'In-Salah'],
    'In Guezzam': ['In Guezzam', 'عين قزام', 'Ain Guezzam', 'In-Guezzam', 'Ain-Guezzam'],
    'Touggourt': ['Touggourt', 'تقرت', 'Tugurt', 'Touggurt', 'Toggourt', 'Teggourt'],
    'Djanet': ['Djanet', 'جانت', 'Janet', 'Djanet Illizi', 'Janet Illizi'],
    'El M\'Ghair': ['El M\'Ghair', 'المغير', 'El Meghaier', 'El-Mgheir', 'El Meghair', 'El-Meghair'],
    'El Meniaa': ['El Meniaa', 'المنيعة', 'El Menia', 'El-Meniaa', 'El-Menia', 'Ghardaia El Meniaa']
}

def load_api_key() -> str:
    """Load Google Maps API key from .env file."""
    load_dotenv()
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        raise ValueError("Please set GOOGLE_MAPS_API_KEY in your .env file")
    return api_key

def initialize_gmaps_client() -> googlemaps.Client:
    """Initialize Google Maps client."""
    api_key = load_api_key()
    return googlemaps.Client(key=api_key)

def get_wilaya_info(address_components: list) -> dict:
    """Extract wilaya information from address components."""
    wilaya_name = next((comp['long_name'] for comp in address_components 
                       if 'administrative_area_level_1' in comp['types']), '')
    
    # Clean up wilaya name
    wilaya_name = wilaya_name.replace('Wilaya d\'', '').replace('Wilaya de ', '')
    
    # Try to find the wilaya info
    for key, info in ALGERIA_WILAYAS.items():
        if key.lower() in wilaya_name.lower():
            return {
                'name': key,
                'code': info['code'],
                'postal_prefix': info['postal_prefix']
            }
    return {'name': wilaya_name, 'code': '', 'postal_prefix': ''}

def extract_postal_code(address_components: list, wilaya_info: dict) -> str:
    """Extract and validate postal code from address components."""
    # Try to get postal code from address components
    postal_code = next((comp['long_name'] for comp in address_components 
                       if 'postal_code' in comp['types']), '')
    
    # If no postal code found, try to extract it from the full address
    if not postal_code:
        for comp in address_components:
            # Look for postal code pattern in any address component
            match = re.search(r'\b\d{5}\b', comp['long_name'])
            if match:
                postal_code = match.group(0)
                break
    
    # Validate postal code format and wilaya prefix
    if postal_code and len(postal_code) == 5:
        prefix = postal_code[:2]
        if prefix == wilaya_info['postal_prefix']:
            return postal_code
    
    # If no valid postal code found, generate a default one using the wilaya prefix
    return f"{wilaya_info['postal_prefix']}000"

def normalize_text(text: str) -> str:
    """Normalize text by removing diacritics and standardizing whitespace."""
    if not text:
        return ''
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Standardize whitespace
    text = ' '.join(text.split())
    return text.lower().strip()

def is_duplicate_location(new_loc: Dict, existing_locations: List[Dict]) -> bool:
    """
    Check if a location is a duplicate using multiple criteria.
    """
    for existing in existing_locations:
        # Check if coordinates are very close (within ~50 meters)
        if abs(new_loc['latitude'] - existing['latitude']) < 0.0005 and \
           abs(new_loc['longitude'] - existing['longitude']) < 0.0005:
            return True
        
        # Check if normalized names and addresses match
        if normalize_text(new_loc['name']) == normalize_text(existing['name']) and \
           normalize_text(new_loc['vicinity'] or '') == normalize_text(existing['vicinity'] or ''):
            return True
        
        # Check if phone numbers match (when available)
        if new_loc.get('phone') and existing.get('phone') and \
           normalize_text(new_loc['phone']) == normalize_text(existing['phone']):
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

def normalize_company_name(company_name: str) -> List[str]:
    """Generate variations of company name for better matching."""
    variations = []
    # Original name
    variations.append(company_name)
    
    # Clean and lowercase
    clean_name = company_name.lower().replace(' ', '')
    variations.append(clean_name)
    
    # Common variations for express/delivery companies
    if 'express' in clean_name.lower():
        # Handle variations like zrexpress, zr express, zr-express
        base_name = clean_name.replace('express', '')
        variations.extend([
            f"{base_name} express",
            f"{base_name}-express",
            f"{base_name}express",
            f"{base_name} delivery",
            f"{base_name} transport"
        ])
        
        # Add variations with spaces
        if len(base_name) > 2:
            variations.extend([
                f"{base_name[:2]} {base_name[2:]} express",
                f"{base_name[:2]}-{base_name[2:]} express",
                f"{base_name[:2]} express"
            ])
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(variations))

def validate_place_name(place_name: str, company_name: str) -> bool:
    """Enhanced validation of place names."""
    if not place_name or not company_name:
        return False
        
    place_normalized = normalize_text(place_name)
    company_variations = normalize_company_name(company_name)
    
    # Check against all variations
    for variation in company_variations:
        variation_normalized = normalize_text(variation)
        if variation_normalized in place_normalized:
            return True
        if place_normalized in variation_normalized:
            return True
        
    # Check for delivery/transport related keywords
    delivery_keywords = ['agence', 'transport', 'livraison', 'delivery', 'express', 'logistics']
    company_simple = normalize_text(company_name).replace(' ', '')
    place_simple = place_normalized.replace(' ', '')
    
    if company_simple in place_simple:
        return True
        
    for keyword in delivery_keywords:
        if keyword in place_normalized and any(var.replace(' ', '') in place_simple for var in company_variations):
            return True
    
    return False

def validate_coordinates(lat: float, lng: float, target_coords: Tuple[float, float], max_distance: float = 0.5) -> bool:
    """Validate coordinates with configurable maximum distance."""
    return (abs(lat - target_coords[0]) <= max_distance and 
            abs(lng - target_coords[1]) <= max_distance)

def process_place_details(details: Dict, wilaya_name: str, lang: str) -> Dict:
    """Process and validate place details with better error handling."""
    try:
        address_components = details.get('address_components', [])
        wilaya_info = get_wilaya_info(address_components)
        
        # Enhanced wilaya name validation
        if not wilaya_info['code']:
            return None
            
        # More flexible wilaya name matching for new wilayas
        wilaya_code = int(wilaya_info['code'])
        if wilaya_code >= 49:
            # For new wilayas, check both current and parent wilaya names
            parent_wilayas = {
                'Timimoun': 'Adrar',
                'Bordj Badji Mokhtar': 'Adrar',
                'Béni Abbès': 'Béchar',
                'In Salah': 'Tamanrasset',
                'In Guezzam': 'Tamanrasset',
                'Touggourt': 'Ouargla',
                'Djanet': 'Illizi',
                'El M\'Ghair': 'El Oued',
                'El Meniaa': 'Ghardaïa'
            }
            if wilaya_name in parent_wilayas:
                if not (wilaya_name.lower() in wilaya_info['name'].lower() or 
                       parent_wilayas[wilaya_name].lower() in wilaya_info['name'].lower()):
                    return None
        elif wilaya_name.lower() not in wilaya_info['name'].lower():
            return None
            
        commune = next((comp['long_name'] for comp in address_components 
                       if 'locality' in comp['types'] or 
                       'sublocality' in comp['types'] or
                       'administrative_area_level_2' in comp['types']), '')
                       
        postal_code = extract_postal_code(address_components, wilaya_info)
        
        # Enhanced location data
        location_data = {
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
            'language': lang,
            'place_id': details.get('place_id', ''),
            'status': details.get('business_status', 'OPERATIONAL')
        }
        
        return location_data
    except Exception as e:
        print(f"Error processing place details: {str(e)}")
        return None

def generate_search_queries(company_name: str, wilaya_name: str) -> List[str]:
    """Generate optimized search queries with enhanced company name handling."""
    queries = []
    company_variations = normalize_company_name(company_name)
    
    # Base queries with company variations
    for variation in company_variations:
        base_queries = [
            f"{variation} {wilaya_name}",
            f"agence {variation} {wilaya_name}",
            f"{variation} livraison {wilaya_name}",
            f"{variation} transport {wilaya_name}"
        ]
        queries.extend(base_queries)
    
    # Special handling for new wilayas (49-58)
    wilaya_code = next((info['code'] for w, info in ALGERIA_WILAYAS.items() if w == wilaya_name), '')
    if wilaya_code and int(wilaya_code) >= 49:
        if wilaya_name in WILAYA_ALTERNATIVES:
            for alt_name in WILAYA_ALTERNATIVES[wilaya_name]:
                for variation in company_variations[:2]:  # Limit variations for alternatives
                    alt_queries = [
                        f"{variation} {alt_name}",
                        f"agence {variation} {alt_name}"
                    ]
                    queries.extend(alt_queries)
        
        # Add parent wilaya references
        parent_wilayas = {
            'Timimoun': 'Adrar',
            'Bordj Badji Mokhtar': 'Adrar',
            'Béni Abbès': 'Béchar',
            'In Salah': 'Tamanrasset',
            'In Guezzam': 'Tamanrasset',
            'Touggourt': 'Ouargla',
            'Djanet': 'Illizi',
            'El M\'Ghair': 'El Oued',
            'El Meniaa': 'Ghardaïa'
        }
        
        if wilaya_name in parent_wilayas:
            parent = parent_wilayas[wilaya_name]
            for variation in company_variations[:2]:
                queries.extend([
                    f"{variation} {wilaya_name} {parent}",
                    f"{variation} agence {parent} {wilaya_name}"
                ])
    
    # Add specific queries for delivery companies
    if any(keyword in company_name.lower() for keyword in ['express', 'delivery', 'transport']):
        for variation in company_variations[:2]:
            delivery_queries = [
                f"{variation} point relais {wilaya_name}",
                f"{variation} depot {wilaya_name}",
                f"{variation} centre {wilaya_name}",
                f"societe {variation} {wilaya_name}",
                f"entreprise {variation} {wilaya_name}"
            ]
            queries.extend(delivery_queries)
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(queries))

def search_in_wilaya(client: googlemaps.Client, company_name: str, wilaya_name: str, 
                    coordinates: Tuple[float, float], language: str) -> List[Dict]:
    locations = []
    queries = generate_search_queries(company_name, wilaya_name)
    
    # Special handling for new wilayas - try with larger radius
    wilaya_code = next((info['code'] for w, info in ALGERIA_WILAYAS.items() if w == wilaya_name), '')
    search_radius = 50000 if wilaya_code and int(wilaya_code) >= 49 else 30000
    
    # For specific wilayas with known issues, try larger radius
    problematic_wilayas = {'Blida', 'Alger', 'Oran', 'Constantine'}
    if wilaya_name in problematic_wilayas:
        search_radius = 40000
    
    try:
        search_result = None
        for query in queries:
            try:
                print(f"Searching with query: {query}")
                search_result = client.places(
                    query,
                    location=coordinates,
                    radius=search_radius,
                    language='fr',
                    type='establishment'
                )
                
                if search_result.get('results'):
                    break
                    
                time.sleep(2)
                
            except Exception as e:
                print(f"Query error for '{query}': {str(e)}")
                time.sleep(2)
                continue

        # Try text search if places search fails
        if not search_result or not search_result.get('results'):
            try:
                print("Trying text search...")
                for variation in normalize_company_name(company_name)[:2]:
                    search_result = client.places(
                        f"{variation} {wilaya_name}",
                        location=coordinates,
                        radius=search_radius,
                        language='fr'
                    )
                    if search_result.get('results'):
                        break
                    time.sleep(2)
            except Exception as e:
                print(f"Text search error: {str(e)}")
                time.sleep(2)

        # Try nearby search as last resort
        if not search_result or not search_result.get('results'):
            try:
                print("Trying nearby search...")
                search_result = client.places_nearby(
                    location=coordinates,
                    radius=search_radius,
                    keyword=company_name,
                    language='fr'
                )
                time.sleep(2)
            except Exception as e:
                print(f"Nearby search error: {str(e)}")
                time.sleep(2)
                return locations

        processed_places = set()
        
        for place in search_result.get('results', []):
            if not validate_place_name(place.get('name', ''), company_name):
                continue
                
            place_id = place['place_id']
            if place_id in processed_places:
                continue
                
            processed_places.add(place_id)
            
            try:
                print(f"Getting details for: {place.get('name', '')}")
                details = client.place(place_id, fields=[
                    'formatted_address',
                    'geometry',
                    'name',
                    'address_component',
                    'vicinity',
                    'international_phone_number',
                    'website',
                    'business_status',
                    'place_id',
                    'type'
                ], language='fr')['result']
                
                if details.get('business_status') == 'CLOSED_PERMANENTLY':
                    continue
                    
                location_data = process_place_details(details, wilaya_name, 'fr')
                
                if location_data and not is_duplicate_location(location_data, locations):
                    # More lenient coordinate validation for problematic wilayas
                    max_distance = 0.8 if wilaya_name in problematic_wilayas else (0.8 if int(wilaya_code) >= 49 else 0.5)
                    if validate_coordinates(location_data['latitude'], location_data['longitude'], coordinates, max_distance):
                        locations.append(location_data)
                        print(f"Found valid location: {location_data['name']} in {wilaya_name}")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Error getting place details: {str(e)}")
                time.sleep(2)
                continue
                
    except Exception as e:
        print(f"Error searching in {wilaya_name}: {str(e)}")
        time.sleep(2)
    
    return locations

def search_company_locations(client: googlemaps.Client, company_name: str, language: str = 'fr') -> List[Dict]:
    """Search for company locations across Algeria."""
    all_locations = []
    total_wilayas = len(WILAYA_COORDINATES)
    
    print(f"\nSearching for {company_name} locations across Algeria...")
    
    for idx, (wilaya_name, coordinates) in enumerate(WILAYA_COORDINATES.items(), 1):
        print(f"\nSearching in {wilaya_name} ({idx}/{total_wilayas})...")
        
        locations = search_in_wilaya(client, company_name, wilaya_name, coordinates, language)
        if locations:
            all_locations.extend(locations)
    
    return all_locations

def save_to_csv(locations: List[Dict], company_name: str):
    """Save the results to a CSV file with enhanced formatting."""
    if not locations:
        print("No locations found.")
        return
    
    # Sort locations by wilaya code and name
    locations.sort(key=lambda x: (x['wilaya_code'], x['name']))
    
    # Create timestamp for unique filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{company_name.replace(' ', '_').lower()}_locations_{timestamp}.csv"
    
    try:
        df = pd.DataFrame(locations)
        # Reorder columns for better readability
        columns_order = [
            'name', 'address', 'wilaya_name', 'wilaya_code', 'commune',
            'postal_code', 'phone', 'website', 'latitude', 'longitude',
            'vicinity', 'language', 'place_id', 'status'
        ]
        df = df[columns_order]
        
        # Ensure proper encoding for Arabic text
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nResults saved to {filename}")
        
        # Print summary
        print(f"\nSummary:")
        print(f"Total locations found: {len(locations)}")
        print("Locations per wilaya:")
        wilaya_counts = df.groupby('wilaya_name').size()
        for wilaya, count in wilaya_counts.items():
            print(f"- {wilaya}: {count}")
            
    except Exception as e:
        print(f"Error saving results: {str(e)}")
        # Fallback save method
        try:
            import json
            backup_file = f"{company_name.replace(' ', '_').lower()}_locations_{timestamp}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(locations, f, ensure_ascii=False, indent=2)
            print(f"Results saved to backup file: {backup_file}")
        except Exception as e2:
            print(f"Error saving backup file: {str(e2)}")

def main():
    try:
        # Get company name from user
        company_name = input("Enter the company name to search: ").strip()
        
        # Get preferred language
        while True:
            lang_choice = input("Choose language (en/fr/both): ").strip().lower()
            if lang_choice in ['en', 'fr', 'both']:
                break
            print("Invalid choice. Please enter 'en', 'fr', or 'both'.")
        
        # Initialize Google Maps client
        client = initialize_gmaps_client()
        
        print(f"\nSearching for {company_name} locations across all wilayas in Algeria...")
        print("This may take several minutes as we search each wilaya...")
        
        # Search for locations
        locations = search_company_locations(client, company_name, lang_choice)
        
        # Display results
        if locations:
            print(f"\nFound {len(locations)} unique location(s):")
            for i, loc in enumerate(locations, 1):
                print(f"\nLocation {i}:")
                print(f"Name: {loc['name']}")
                print(f"Address: {loc['address']}")
                print(f"Vicinity: {loc['vicinity']}")
                print(f"Wilaya: {loc['wilaya_name']} (Code: {loc['wilaya_code']})")
                print(f"Commune: {loc['commune']}")
                print(f"Postal Code: {loc['postal_code']}")
                if loc['phone']:
                    print(f"Phone: {loc['phone']}")
                print(f"Coordinates: {loc['latitude']}, {loc['longitude']}")
                print(f"Language: {loc['language']}")
            
            # Save results to CSV
            save_to_csv(locations, company_name)
        else:
            print(f"\nNo locations found for {company_name} in Algeria.")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 