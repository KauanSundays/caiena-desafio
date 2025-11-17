import os
import requests
from dotenv import load_dotenv

load_dotenv() 

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") 
GEO_API_URL = os.getenv("GEO_API_URL") 

def get_city_coordinates(city_query: str) -> dict or None:
    try:
        params = {
            'q': city_query,
            'limit': 1,
            'appid': OPENWEATHER_API_KEY
        }
        print(params)
        
        response = requests.get(GEO_API_URL, params=params)
        response.raise_for_status()

        geo_data = response.json()
        
        if geo_data:
            city_data = geo_data[0]
            return {
                'lat': city_data.get('lat'),
                'lon': city_data.get('lon')
            }
        else:
            print(f"A cidade '{city_query}' não foi encontrada na api")
            return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

if __name__ == "__main__":
    test_city = "São Paulo,BR"
    print(f"--- Testando SDK para {test_city} ---")
    coords = get_city_coordinates(test_city)
    if coords:
        print(f"Lat: {coords['lat']}, Lon: {coords['lon']}")
    print("-----------------------------------")
