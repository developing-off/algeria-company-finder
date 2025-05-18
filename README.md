# Algeria Company Location Finder

This application helps you find all locations of a specific company in Algeria using Google Maps API, including details like address, wilaya, commune, and zip code.

## Setup

<<<<<<< HEAD
1. Install the required dependencies:
=======
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
git clone https://github.com/developing-off/algeria-company-finder.git
cd algeria-company-finder
```

2. Install dependencies:
>>>>>>> ff4fa5aa00ad038e7037c54635ea0e93dddf3948
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and add your Google Maps API key:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

To get a Google Maps API key:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Places API and Maps JavaScript API
4. Create credentials (API key)
5. Copy the API key to your `.env` file

## Usage

Run the script with:
```bash
python company_finder.py
```

<<<<<<< HEAD
Enter the company name when prompted, and the application will search for all locations in Algeria. 
=======
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

I'm Younes Sarni, a tech entrepreneur and fullstack developer based in Oran, Algeria. As the founder of an e-commerce platform, I created this tool to solve real-world challenges in the Algerian market, particularly the lack of public APIs for delivery company locations.

Connect with me:
- LinkedIn: [Younes Sarni](https://dz.linkedin.com/in/younesarni)
- Email: sarniyounes@gmail.com
- Website: [younes-sarni.me](https://ys-dev.tech)
- Twitter: [@sarni_younes](https://twitter.com/sarni_younes)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Maps API for providing reliable location data
- The Python community for excellent libraries
- The Algerian tech community for feedback and support

---

Made with ❤️ in Algeria 🇩🇿 
>>>>>>> ff4fa5aa00ad038e7037c54635ea0e93dddf3948
