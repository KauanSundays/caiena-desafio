from openweather_sdk import get_city_coordinates, get_5_days_forecast

CITY_QUERY = "Rio de Janeiro,BR"

coords = get_city_coordinates(CITY_QUERY)

print("-" * 40)

if coords:
    print(f"Coordenadas encontradas para {CITY_QUERY}:")
    print(f"Latitude (lat): {coords['lat']}")
    print(f"Longitude (lon): {coords['lon']}")
    
    forecast_5_days = get_5_days_forecast(coords['lat'], coords['lon'])
    print(forecast_5_days)
else:
    print(f"Não foi possível obter coordenadas para {CITY_QUERY}. Verifique a chave da API e o nome da cidade.")


print("-" * 40)
