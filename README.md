# Algeria Company Location Finder

This application helps you find all locations of a specific company in Algeria using Google Maps API, including details like address, wilaya, commune, and zip code.

## Setup

1. Install the required dependencies:
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

Enter the company name when prompted, and the application will search for all locations in Algeria. 