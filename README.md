# Algeria Company Location Finder 🌍

## Overview

As the founder of an e-commerce platform in Algeria, I developed this tool to solve a critical business need. While working with delivery companies like ZRexpress, I noticed they lacked public APIs to fetch their stopdesk locations. This script helps businesses and developers easily find all locations of any company across Algeria's 58 wilayas.

## Features

- 🔍 Comprehensive search across all 58 Algerian wilayas
- 🌐 Multi-language support (Arabic, French, English)
- 📍 Accurate location data with coordinates
- 📱 Phone number standardization
- 🏢 Complete address information (wilaya, commune, postal code)
- 📊 CSV export for easy data integration
- 🔄 Duplicate detection and validation
- 🗺️ Uses Google Maps API for reliable data

## Prerequisites

- Python 3.8+
- Google Maps API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/algeria-company-finder.git
cd algeria-company-finder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google Maps API key:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## Usage

Run the script:
```bash
python company_finder.py
```

Follow the prompts to:
1. Enter the company name to search
2. Choose the preferred language (en/fr/both)
3. Wait for the results

The script will:
- Search all wilayas for company locations
- Display found locations with details
- Save results to a CSV file

## Example Output

The script generates a CSV file with the following information for each location:
- Company name
- Complete address
- Wilaya name and code
- Commune
- Postal code
- Phone number (if available)
- Coordinates (latitude/longitude)
- Website (if available)

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Use Cases

- E-commerce platforms needing delivery points
- Logistics companies mapping service coverage
- Businesses planning expansion strategies
- Market researchers analyzing company presence

## About the Author

I'm a tech entrepreneur and developer based in Algeria, focused on improving the e-commerce and logistics ecosystem. I created this tool while building my e-commerce platform to solve real-world challenges in the Algerian market.

Connect with me on [LinkedIn](https://www.linkedin.com/in/YOUR_LINKEDIN_USERNAME)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Maps API for providing reliable location data
- The Python community for excellent libraries
- The Algerian tech community for feedback and support

---

Made with ❤️ in Algeria 🇩🇿 