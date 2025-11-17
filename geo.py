import requests
import os
from dotenv import load_dotenv
load_dotenv() 

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") 
CITY_QUERY = "Rio de Janeiro,BR"
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"

if not OPENWEATHER_API_KEY:
    print("chave não funcionoou ainda.")
    exit()
try:
    params = {'q': CITY_QUERY, 'limit': 1, 'appid': OPENWEATHER_API_KEY}
    
    response = requests.get(GEOCODING_URL, params=params)
    response.raise_for_status()
    geo_data = response.json()
    if geo_data:
        # print(geo_data)
        city_data = geo_data[0]
        print(city_data['lat'])
        print(city_data['lon'])
    else:
      print("Não encontrado")
except requests.exceptions.RequestException as e:
    print(f" Erro na requisição: {e}")
    
print("-" * 30)
