import unittest
import json
from unittest.mock import patch
from app import app 

# Mensagem formatada que o MOCK irá retornar
EXPECTED_GIST_MESSAGE = (
    "30°C e sol em São Paulo,BR em 17/11. Média para os próximos dias: "
    "31°C em 18/11, 31°C em 19/11, 31°C em 20/11, 31°C em 21/11, e 31°C em 22/11"
)

# Dados simulados para a previsão
MOCK_FORECAST_DATA = {
    'current_temp': 30,
    'current_description': 'sol',
    'current_date': '17/11',
    'forecast_days': [
        {'date': '18/11', 'temp': 31},
        {'date': '19/11', 'temp': 31},
        {'date': '20/11', 'temp': 31},
        {'date': '21/11', 'temp': 31},
        {'date': '22/11', 'temp': 31},
    ] 
}

class TestAPISuccess(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # O mock de format_weather_message agora retorna a string que queremos verificar
    
    @patch('app.get_city_coordinates', return_value={'lat': -23.55, 'lon': -46.63})
    @patch('app.get_5_days_forecast', return_value=MOCK_FORECAST_DATA)
    @patch('app.post_comment_to_gist', return_value=True)
    @patch('app.format_weather_message', return_value=EXPECTED_GIST_MESSAGE)
    def test_previsao_success_scenario_with_message_check(self, mock_format, mock_post, mock_forecast, mock_coords):
        """
        Testa o cenário completo de sucesso e verifica a mensagem final formatada.
        """
        test_city = "Sao Paulo,BR"
        
        response = self.app.get(f'/previsao?cidade={test_city}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200, "Deve retornar status 200 (OK)")
        print("\n--- MENSAGEM FINAL PARA O GIST ---")
        print(data['mensagem_enviada'])
        print("----------------------------------\n")
        
        self.assertEqual(data['mensagem_enviada'], EXPECTED_GIST_MESSAGE, 
                         "A mensagem no JSON de resposta deve ser a esperada.")
        
        # Confirma que a função de postagem foi chamada com a mensagem correta
        mock_post.assert_called_once_with(EXPECTED_GIST_MESSAGE)

if __name__ == '__main__':
    unittest.main()
