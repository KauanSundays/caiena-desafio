from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv() 

from src.sdk.openweather_sdk import get_city_coordinates, get_5_days_forecast, format_weather_message
from src.services.github_service import post_comment_to_gist

app = Flask(__name__)

@app.route('/previsao', methods=['GET'])
def get_weather_and_post_gist():
    city_query = request.args.get('cidade')
    
    if not city_query:
        return jsonify({
            "status": "erro", 
            "mensagem": "parametro cidade'é obrigatório. Ex: /previsao?cidade=Sao Paulo,BR"
        }), 400

    print(f"\n--- Processando requisição para: {city_query} ---")
    
    coords = get_city_coordinates(city_query)
    
    if not coords:
        return jsonify({
            "status": "erro", 
            "mensagem": f"Não foi possível encontrar a cidade: {city_query}"
        }), 404
    
    forecast_5_days = get_5_days_forecast(coords['lat'], coords['lon'])
    
    if not forecast_5_days:
        return jsonify({
            "status": "erro", 
            "mensagem": f"Coordenadas encontradas, mas falha ao obter previsão para {city_query}"
        }), 500
        
    final_message = format_weather_message(city_query, forecast_5_days)
    
    post_success = post_comment_to_gist(final_message)
    
    if post_success:
        return jsonify({
            "status": "sucesso",
            "cidade_processada": city_query,
            "mensagem_enviada": final_message,
            "detalhes": "Comentário enviado com sucesso para o Gist."
        }), 200
    else:
        return jsonify({
            "status": "erro",
            "cidade_processada": city_query,
            "mensagem": "Falha ao enviar comentário para o GitHub Gist. Verifique logs do servidor e .env."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
