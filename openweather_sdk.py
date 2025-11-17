import os
import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv() 

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") 
OPENWEATHER_URL_5_DAYS = os.getenv("OPENWEATHER_URL_5_DAYS") 
GEO_URL = os.getenv("GEO_API_URL") 

def get_city_coordinates(city_query: str) -> dict or None:
    try:
        params = {
            'q': city_query,
            'limit': 1,
            'appid': OPENWEATHER_API_KEY
        }
        print(params)
        
        response = requests.get(GEO_URL, params=params)
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
    
def get_5_days_forecast(lat: float, lon: float) -> dict or None:
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',
            'lang': 'pt_br'
        }
        
        response = requests.get(OPENWEATHER_URL_5_DAYS, params=params)
        print(params)
        response.raise_for_status()

        data = response.json()
        
        if 'list' not in data:
            print("Erro: Dados de previsão vazios.")
            return None

        current_data = data['list'][0]
        current_temp = round(current_data['main']['temp'])
        current_description = current_data['weather'][0]['description']

        daily_temps = {}
        for item in data['list']:
            dt_txt = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            temp = item['main']['temp']
            
            if dt_txt not in daily_temps:
                daily_temps[dt_txt] = []
            daily_temps[dt_txt].append(temp)

        forecast_days = []
        # Ignora o dia atual, pega  5 próximas datas
        sorted_dates = sorted(daily_temps.keys())[1:6] 

        for date_str in sorted_dates:
            temps = daily_temps[date_str]
            avg_temp = round(sum(temps) / len(temps))
            formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m')
            
            forecast_days.append({
                'date': formatted_date,
                'temp': avg_temp
            })

        return {
            'current_temp': current_temp,
            'current_description': current_description,
            'current_date': datetime.now().strftime('%d/%m'),
            'forecast_days': forecast_days
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição de Forecast: {e}")
        return None
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado no Forecast: {e}")
        return None
    
if __name__ == "__main__":
    test_city = "São Paulo,BR"
    print(f"--- Testando SDK para {test_city} ---")
    coords = get_city_coordinates(test_city)
    if coords:
        print(f"Lat: {coords['lat']}, Lon: {coords['lon']}")
    print("-----------------------------------")
