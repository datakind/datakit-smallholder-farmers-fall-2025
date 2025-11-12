#!/usr/bin/env python3
"""
Download Weather Data from NASA POWER API

This script downloads daily weather data for Kenya, Uganda, and Tanzania
from the NASA POWER API for the period 2015-2022.

Parameters downloaded:
- T2M: Temperature at 2 Meters (°C)
- T2M_MAX: Maximum Temperature at 2 Meters (°C)
- T2M_MIN: Minimum Temperature at 2 Meters (°C)
- PRECTOTCORR: Precipitation Corrected (mm/day)
- RH2M: Relative Humidity at 2 Meters (%)
- WS2M: Wind Speed at 2 Meters (m/s)

Usage:
    python3 download_weather_data.py
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import time

# Configuration
BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
START_DATE = "20150101"
END_DATE = "20221231"
PARAMETERS = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M']

# Country coordinates (capital cities as reference points)
LOCATIONS = {
    'kenya': {
        'name': 'Nairobi',
        'latitude': -1.2921,
        'longitude': 36.8219
    },
    'uganda': {
        'name': 'Kampala',
        'latitude': 0.3476,
        'longitude': 32.5825
    },
    'tanzania': {
        'name': 'Dodoma',
        'latitude': -6.1630,
        'longitude': 35.7516
    }
}

# Additional regional locations for better coverage
REGIONAL_LOCATIONS = {
    'kenya_mombasa': {'latitude': -4.0435, 'longitude': 39.6682},
    'kenya_kisumu': {'latitude': -0.0917, 'longitude': 34.7680},
    'uganda_gulu': {'latitude': 2.7746, 'longitude': 32.2989},
    'tanzania_dar': {'latitude': -6.7924, 'longitude': 39.2083},
    'tanzania_arusha': {'latitude': -3.3869, 'longitude': 36.6830}
}

def get_weather_data(latitude, longitude, start_date, end_date, parameters):
    """
    Fetch weather data from NASA POWER API
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        start_date (str): Start date in YYYYMMDD format
        end_date (str): End date in YYYYMMDD format
        parameters (list): List of parameter names
    
    Returns:
        pandas.DataFrame: Weather data with datetime index
    """
    params = {
        'parameters': ','.join(parameters),
        'community': 'AG',  # Agroclimatology community
        'longitude': longitude,
        'latitude': latitude,
        'start': start_date,
        'end': end_date,
        'format': 'JSON'
    }
    
    print(f"Requesting data for ({latitude}, {longitude})...")
    print(f"URL: {BASE_URL}")
    print(f"Parameters: {params}")
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if request was successful
        if 'properties' not in data or 'parameter' not in data['properties']:
            print(f"Error: Unexpected response structure")
            print(f"Response: {json.dumps(data, indent=2)[:500]}")
            return None
        
        # Extract parameter data
        df_list = []
        for param in parameters:
            if param in data['properties']['parameter']:
                param_data = data['properties']['parameter'][param]
                df_param = pd.DataFrame(list(param_data.items()), 
                                       columns=['date', param])
                df_list.append(df_param.set_index('date'))
            else:
                print(f"Warning: Parameter {param} not found in response")
        
        if not df_list:
            print("Error: No parameter data found")
            return None
        
        # Combine all parameters
        df = pd.concat(df_list, axis=1)
        
        # Convert index to datetime
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        
        # Replace missing value indicator (-999) with NaN
        df = df.replace(-999, pd.NA)
        
        # Add metadata columns
        df['latitude'] = latitude
        df['longitude'] = longitude
        
        print(f"Successfully downloaded {len(df)} days of data")
        print(f"Date range: {df.index.min()} to {df.index.max()}")
        print(f"Missing values: {df.isna().sum().to_dict()}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def download_country_data(country, location_info, output_dir):
    """
    Download weather data for a country
    
    Args:
        country (str): Country name
        location_info (dict): Location information with latitude and longitude
        output_dir (Path): Output directory path
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Downloading data for {country.upper()} ({location_info['name']})")
    print(f"{'='*60}")
    
    df = get_weather_data(
        latitude=location_info['latitude'],
        longitude=location_info['longitude'],
        start_date=START_DATE,
        end_date=END_DATE,
        parameters=PARAMETERS
    )
    
    if df is not None:
        # Save to CSV
        output_file = output_dir / f"weather_{country}.csv"
        df.to_csv(output_file)
        print(f"Saved to: {output_file}")
        
        # Save metadata
        metadata = {
            'country': country,
            'location': location_info['name'],
            'latitude': location_info['latitude'],
            'longitude': location_info['longitude'],
            'start_date': START_DATE,
            'end_date': END_DATE,
            'parameters': PARAMETERS,
            'download_timestamp': datetime.now().isoformat(),
            'total_days': len(df),
            'missing_values': df.isna().sum().to_dict()
        }
        
        metadata_file = output_dir / f"weather_{country}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to: {metadata_file}")
        
        return True
    else:
        print(f"Failed to download data for {country}")
        return False

def main():
    """Main function to download all weather data"""
    print("="*60)
    print("NASA POWER Weather Data Download")
    print("="*60)
    print(f"Date range: {START_DATE} to {END_DATE}")
    print(f"Parameters: {', '.join(PARAMETERS)}")
    print(f"Countries: {', '.join(LOCATIONS.keys())}")
    print("="*60)
    
    # Create output directory
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    output_dir = project_dir / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nOutput directory: {output_dir}")
    
    # Download data for each country
    results = {}
    for country, location_info in LOCATIONS.items():
        success = download_country_data(country, location_info, output_dir)
        results[country] = success
        
        # Be nice to the API - wait between requests
        if country != list(LOCATIONS.keys())[-1]:  # Don't wait after last request
            print("\nWaiting 2 seconds before next request...")
            time.sleep(2)
    
    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    for country, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{country.upper()}: {status}")
    
    total_success = sum(results.values())
    print(f"\nTotal: {total_success}/{len(results)} countries downloaded successfully")
    
    if total_success == len(results):
        print("\n✓ All data downloaded successfully!")
        print(f"\nNext steps:")
        print(f"1. Check the data files in: {output_dir}")
        print(f"2. Run preprocessing: python3 scripts/preprocess_questions.py")
        print(f"3. Start analysis: jupyter notebook notebooks/03_exploratory_analysis.ipynb")
    else:
        print("\n⚠ Some downloads failed. Please check the errors above.")
        print("You may need to retry or check your internet connection.")
    
    print("="*60)

if __name__ == "__main__":
    main()
