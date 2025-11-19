import pytest
from unittest.mock import patch
import json
from src.api.app import app 


APP_MODULE_PATH = 'src.api.app' 

EXPECTED_GIST_MESSAGE = (
    "30°C e sol em São Paulo,BR em 17/11. Média para os próximos dias: "
    "31°C em 18/11, 31°C em 19/11, 31°C em 20/11, 31°C em 21/11, e 31°C em 22/11"
)

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

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch(f'{APP_MODULE_PATH}.get_city_coordinates', return_value={'lat': -23.55, 'lon': -46.63})
@patch(f'{APP_MODULE_PATH}.get_5_days_forecast', return_value=MOCK_FORECAST_DATA)
@patch(f'{APP_MODULE_PATH}.post_comment_to_gist', return_value=True)
@patch(f'{APP_MODULE_PATH}.format_weather_message', return_value=EXPECTED_GIST_MESSAGE)

def test_previsao_success_scenario(mock_format, mock_post, mock_forecast, mock_coords, client):
    """ Testa o cenário completo de sucesso (200 OK). """
    test_city = "Sao Paulo,BR"
    
    response = client.get(f'/previsao?cidade={test_city}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    
    assert data['status'] == 'sucesso'
    assert data['mensagem_enviada'] == EXPECTED_GIST_MESSAGE
    
    mock_post.assert_called_once_with(EXPECTED_GIST_MESSAGE)


# 2. Teste de Erro 400 (Parâmetro Ausente)
def test_previsao_missing_city_param(client):
    """ Verifica se a API retorna 400 quando o parâmetro 'cidade' está ausente. """
    response = client.get('/previsao')
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'erro'
    assert "parametro cidade'é obrigatório" in data['mensagem']

# 3. teste de erro 404 (cidade nao encontrada)
@patch(f'{APP_MODULE_PATH}.get_city_coordinates', return_value=None)
def test_previsao_city_not_found(mock_coords, client):
    """ Verifica se a API retorna 404 quando o SDK não encontra as coordenadas. """
    response = client.get('/previsao?cidade=CidadeInexistente')
    
    assert response.status_code == 404
    assert json.loads(response.data)['status'] == 'erro'
    mock_coords.assert_called_once()

# 4. teste de erro 500 (Falha na Previsão do Tempo)
@patch(f'{APP_MODULE_PATH}.get_city_coordinates', return_value={'lat': -23.55, 'lon': -46.63})
@patch(f'{APP_MODULE_PATH}.get_5_days_forecast', return_value=None)
def test_previsao_forecast_failure(mock_forecast, mock_coords, client):
    response = client.get('/previsao?cidade=Sao Paulo,BR')
    data = json.loads(response.data)
    
    assert response.status_code == 500
    assert data['status'] == 'erro'
    assert "falha ao obter previsão" in data['mensagem']

# 5. teste de erro 500 (falha ao postar no gist)
@patch(f'{APP_MODULE_PATH}.get_city_coordinates', return_value={'lat': -23.55, 'lon': -46.63})
@patch(f'{APP_MODULE_PATH}.get_5_days_forecast', return_value=MOCK_FORECAST_DATA)
@patch(f'{APP_MODULE_PATH}.post_comment_to_gist', return_value=False)
@patch(f'{APP_MODULE_PATH}.format_weather_message', return_value='Previsão formatada de teste')
def test_previsao_gist_post_failure_corrected(mock_format, mock_post, mock_forecast, mock_coords, client):
    """ Verifica se a API retorna 500 quando falha ao postar o comentário no Gist. """
    response = client.get('/previsao?cidade=Sao Paulo,BR')
    data = json.loads(response.data)
    
    assert response.status_code == 500
    assert data['status'] == 'erro'
    assert "Falha ao enviar comentário para o GitHub Gist" in data['mensagem'] 
    mock_post.assert_called_once()
