from openweather_sdk import get_city_coordinates, get_5_days_forecast, format_weather_message
from github_service import post_comment_to_gist

CITY_QUERY = "Rio de Janeiro,BR"

coords = get_city_coordinates(CITY_QUERY)

print("-" * 40)

if coords:
    print(f"Coordenadas encontradas para {coords.get('city_name')}:")
    print(f"Latitude (lat): {coords['lat']}")
    print(f"Longitude (lon): {coords['lon']}")
    
    forecast_5_days = get_5_days_forecast(coords['lat'], coords['lon'])
    
    if forecast_5_days:
        final_message = format_weather_message(CITY_QUERY, forecast_5_days)
        
        post_comment_to_gist(final_message)
    else:
        print("\nNão foi possível obter a previsão de 5 dias.")
else:
    print(f"Não foi possível obter coordenadas para {CITY_QUERY}. Verifique a chave da API e o nome da cidade.")


print("-" * 40)
