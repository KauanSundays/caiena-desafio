import requests
import json
import os 

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY_NAME = "London,UK"
UNITS = "metric"
LANG = "pt"

#  temntando recriar exemplo de documentação da OpenWeatherMap
# https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&exclude=hourly,daily&appid={API key}
CURRENT_WEATHER_URL = " https://api.openweathermap.org/data/3.0/onecall"

params = {
    'q': CITY_NAME,
    'appid': OPENWEATHER_API_KEY,
    'units': UNITS,
    'lang': LANG
}

print(f"Buscando clima atual para: {CITY_NAME}...")
print("-" * 30)

try:
    response = requests.get(CURRENT_WEATHER_URL, params=params)
    response.raise_for_status()
    data = response.json()

    temp_atual = data['main']['temp']
    descricao = data['weather'][0]['description']
    cidade = data['name']
    
    print(f"Requisição bem-sucedida! Status HTTP: {response.status_code}")
    print(f"Clima atual em {cidade}:")
    print(f"  Temperatura: {temp_atual}°C")
    print(f"  Condição: {descricao.capitalize()}")

except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP: {e}")
    print(f"Resposta da API: {e.response.text}")
    
except requests.exceptions.RequestException as e:
    print(f"Erro de Conexão: {e}")
    
except KeyError as e:
    print(f"Erro ao processar o JSON: Chave faltando: {e}")

print("-" * 30)
